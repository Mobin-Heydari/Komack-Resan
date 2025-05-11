from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Invoice
from .serializers import InvoiceSerializer
from .permissions import IsInvoiceAdmin

class InvoiceViewSet(viewsets.ViewSet):
    """
    ViewSet for managing Invoice objects.

    Endpoints:
      - List:      GET /invoices/?company_slug=<slug>
           • If request.user.is_staff, returns all invoices (or filtered by company_slug if provided).
           • If request.user.user_type == "OW", returns invoices for companies where the user is the owner.
           • Otherwise, returns a 403 error.
      - Retrieve:  GET /invoices/<pk>/
           • Only accessible if the request user is an admin or (if not admin) they must have an associated company 
             that matches the invoice’s company.
      - Update:    PUT/PATCH /invoices/<pk>/update/
           • Delegated to the custom permission class (IsInvoiceAdmin).

    Note: Creation is restricted to the program/admin only.
    """
    permission_classes = [IsInvoiceAdmin]
    
    def list(self, request):
        # If a company_slug query parameter is provided, filter by that.
        company_slug = request.query_params.get('company_slug')
        if company_slug is not None:
            if request.user.is_staff:
                queryset = Invoice.objects.filter(company__slug=company_slug)
            elif getattr(request.user, 'user_type', None) == "OW":
                queryset = Invoice.objects.filter(company__slug=company_slug, company__employer=request.user)
            else:
                return Response(
                    {"detail": "You do not have permission to list invoices for this company."},
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            # No company_slug provided.
            if request.user.is_staff:
                queryset = Invoice.objects.all()
            elif getattr(request.user, 'user_type', None) == "OW":
                queryset = Invoice.objects.filter(company__employer=request.user)
            else:
                return Response(
                    {"detail": "You do not have permission to list invoices."},
                    status=status.HTTP_403_FORBIDDEN
                )
        serializer = InvoiceSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        invoice = get_object_or_404(Invoice, pk=pk)
        # Allow access if the user is admin.
        if not request.user.is_staff:
            # Otherwise, the user must be a company employer—that is,
            # they must have an associated company, and that company must match the invoice's.
            user_company = getattr(request.user, 'company', None)
            if not user_company or invoice.company != user_company:
                return Response(
                    {"detail": "You do not have permission to access this invoice."},
                    status=status.HTTP_403_FORBIDDEN
                )
        serializer = InvoiceSerializer(invoice, context={'request': request})
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        invoice = get_object_or_404(Invoice, pk=pk)
        # Delegate permission enforcement (update permissions are handled by IsInvoiceAdmin).
        self.check_object_permissions(request, invoice)
        serializer = InvoiceSerializer(invoice, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            updated_invoice = serializer.save()
            response_serializer = InvoiceSerializer(updated_invoice, context={'request': request})
            return Response({
                "message": "Invoice updated successfully.",
                "data": response_serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
