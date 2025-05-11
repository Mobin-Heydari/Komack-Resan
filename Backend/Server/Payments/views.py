from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import PaymentInvoice
from .serializers import PaymentInvoiceSerializer
from .permissions import PaymentInvoicePermission



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
