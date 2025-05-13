from django.shortcuts import get_object_or_404
from django.conf import settings

from rest_framework import viewsets, status, permissions
from rest_framework.views import Response, APIView

from .models import PaymentInvoice
from .serializers import PaymentInvoiceSerializer
from .permissions import PaymentInvoicePermission

from Invoices.models import Invoice

import requests

import json





class PaymentInvoiceViewSet(viewsets.ViewSet):
    """
    A ViewSet for managing PaymentInvoice objects.

    Endpoints:
      - List:      GET /payment-invoices/
          * If admin (is_staff), returns all PaymentInvoice objects.
          * If company employer (user_type "OW"), returns PaymentInvoice objects where
            invoice.company.owner equals the requesting user.
      - Create:    POST /payment-invoices/create/
          * Allowed only for company employers (OW); additional invoice validation is done by the serializer.
      - Retrieve:  GET /payment-invoices/<pk>/
          * Only admin can retrieve any PaymentInvoice,
          * and a non-admin can retrieve only if the invoice’s company owner matches request.user.
      - Update:    PUT/PATCH /payment-invoices/<pk>/update/
          * Only admin users are allowed to update PaymentInvoice records.
    """
    permission_classes = [PaymentInvoicePermission]

    def list(self, request):
        # Admin can see everything.
        if request.user.is_staff:
            queryset = PaymentInvoice.objects.all()
        # Company employer (OW) gets only payments for their own invoices.
        elif getattr(request.user, 'user_type', None) == "OW":
            queryset = PaymentInvoice.objects.filter(invoice__company__owner=request.user)
        else:
            return Response(
                {"detail": "You do not have permission to list payment records."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = PaymentInvoiceSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        serializer = PaymentInvoiceSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            instance = serializer.save()
            response_serializer = PaymentInvoiceSerializer(instance, context={'request': request})
            return Response(
                {
                    "message": "Payment created successfully.",
                    "data": response_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        instance = get_object_or_404(PaymentInvoice, pk=pk)
        # For non-admin users, ensure that the payment's invoice company is owned by the request user.
        if not request.user.is_staff:
            if instance.invoice.company.employer != request.user:
                return Response(
                    {"detail": "You do not have permission to access this payment."},
                    status=status.HTTP_403_FORBIDDEN
                )
        serializer = PaymentInvoiceSerializer(instance, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = get_object_or_404(PaymentInvoice, pk=pk)
        # Permission for update is delegated to the custom permission class, which allows only admin.
        self.check_object_permissions(request, instance)
        serializer = PaymentInvoiceSerializer(instance, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            instance = serializer.save()
            response_serializer = PaymentInvoiceSerializer(instance, context={'request': request})
            return Response(
                {
                    "message": "Payment updated successfully.",
                    "data": response_serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def get_invoice_description(invoice):
    return f"پرداخت فاکتور شماره: {invoice.id}"

class SendPaymentRequest(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, invoice_id):
        invoice = get_object_or_404(Invoice, id=invoice_id)

        # Verify that the logged-in user is authorized to pay for the invoice.
        if invoice.company.employer != request.user:
            return Response(
                {"message": "شما برای پرداخت این سفارش مجوز ندارید."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Create or retrieve the PaymentInvoice associated with the invoice.
        payment_invoice, created = PaymentInvoice.objects.get_or_create(
            invoice=invoice,
            defaults={
                "amount": invoice.total_amount,
                "payment_status": PaymentInvoice.PaymentStatusChoices.PENDING,
            }
        )

        description = get_invoice_description(invoice)
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": invoice.total_amount,
            "Description": description,
            "CallbackURL": settings.CallbackURL,  # Ensure you pass the callback URL from settings.
            "metadata": {
                "Email": request.user.email,
                "mobile": request.user.phone,
                "invoice_id": invoice_id,
                "payment_invoice_id": str(payment_invoice.id)
            },
        }

        json_data = json.dumps(data)
        headers = {
            'Content-Type': 'application/json',
            'Content-Length': str(len(json_data))
        }

        try:
            response = requests.post(settings.ZP_API_REQUEST, data=json_data, headers=headers, timeout=10)
        except requests.exceptions.Timeout:
            return Response({'status': False, 'code': 'timeout'}, status=status.HTTP_408_REQUEST_TIMEOUT)
        except requests.exceptions.ConnectionError:
            return Response({'status': False, 'code': 'connection error'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('Status') == 100:
                authority = response_data.get('Authority')
                # Save the authority into the PaymentInvoice record.
                payment_invoice.authority = authority
                payment_invoice.save()

                # Build the payment URL by appending the authority as a GET parameter.
                # The final URL will look like:  
                #   https://{sandbox}.zarinpal.com/pg/StartPay/?Authority={authority}
                payment_url = f"{settings.ZP_API_STARTPAY}?Authority={authority}"
                return Response({
                    'status': True,
                    'url': payment_url,
                    'authority': authority,
                    'payment_invoice_id': str(payment_invoice.id)
                })
            else:
                return Response({'status': False, 'code': str(response_data.get('Status'))},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response({'status': False, 'code': 'unexpected error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class VerifyPaymentRequest(APIView):
    # The callback endpoint is accessed without user authentication.
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # Get the authority from the GET parameters; Zarinpal provides this in the callback.
        authority = request.GET.get('Authority')
        if not authority:
            return Response({"message": "پارامتر Authority ارسال نشده است."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Locate the PaymentInvoice using the authority.
            payment_invoice = PaymentInvoice.objects.get(authority=authority)
        except PaymentInvoice.DoesNotExist:
            return Response({"message": "رکورد پرداخت یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        invoice = payment_invoice.invoice
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": invoice.total_amount,
            "Authority": authority,
        }
        json_data = json.dumps(data)
        headers = {
            'Content-Type': 'application/json',
            'Content-Length': str(len(json_data))
        }

        try:
            response = requests.post(settings.ZP_API_VERIFY, data=json_data, headers=headers, timeout=10)
        except requests.exceptions.Timeout:
            payment_invoice.payment_status = PaymentInvoice.PaymentStatusChoices.FAILED
            payment_invoice.save()
            return Response({"message": "Timeout during verification."}, status=status.HTTP_408_REQUEST_TIMEOUT)
        except requests.exceptions.ConnectionError:
            payment_invoice.payment_status = PaymentInvoice.PaymentStatusChoices.FAILED
            payment_invoice.save()
            return Response({"message": "Connection error during verification."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('Status') == 100:
                # Capture the transaction ID (RefID) returned by Zarinpal.
                payment_invoice.transaction_id = response_data.get('RefID')
                payment_invoice.mark_successful()
                return Response({"message": "پرداخت با موفقیت انجام شد."})
            else:
                payment_invoice.payment_status = PaymentInvoice.PaymentStatusChoices.FAILED
                payment_invoice.save()
                return Response({"message": "پرداخت با شکست مواجه شد."}, status=status.HTTP_417_EXPECTATION_FAILED)

        payment_invoice.payment_status = PaymentInvoice.PaymentStatusChoices.FAILED
        payment_invoice.save()
        return Response({"message": "خطای غیرمنتظره در بررسی تراکنش."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
