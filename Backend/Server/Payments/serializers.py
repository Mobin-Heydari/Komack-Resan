from rest_framework import serializers
from .models import PaymentInvoice
from Invoices.models import Invoice
from Invoices.serializers import InvoiceSerializer  # Existing serializer for Invoice details



class PaymentInvoiceSerializer(serializers.ModelSerializer):

    # Nested display of the invoice details.
    invoice = InvoiceSerializer(read_only=True)
    # For write operations, accept an invoice_id.
    invoice_id = serializers.CharField(
        write_only=True,
        required=False,
        help_text="The UUID of the invoice for which this payment is made."
    )
    

    class Meta:
        model = PaymentInvoice
        fields = [
            'id',               # UUID primary key
            'invoice',          # Nested invoice details (read-only)
            'invoice_id',       # Write-only field for providing invoice ID
            'amount',
            'transaction_id',
            'payment_status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'invoice', 'created_at', 'updated_at']


    def validate(self, attrs):
        """
        Validate input for both create and update operations.
        
        On creation (when self.instance is None):
          - Ensure an invoice_id is provided.
          - Retrieve the invoice using the provided invoice_id.
          - Ensure the invoice is not already paid.
          - Ensure no PaymentInvoice already exists for the invoice.
          - Add the retrieved invoice to the validated data.
        
        On update:
          - Do not allow updating the invoice association; if an invoice_id is supplied, raise an error.
        """
        request_data = self.context.get('request').data
        invoice_id = request_data.get('invoice_id')
        
        if not self.instance:  # Create operation
            if not invoice_id:
                raise serializers.ValidationError({
                    "invoice_id": "This field is required for creating a payment."
                })
            try:
                invoice = Invoice.objects.get(id=invoice_id)
            except Invoice.DoesNotExist:
                raise serializers.ValidationError({
                    "invoice_id": "Invoice with the provided ID does not exist."
                })
            if invoice.is_paid:
                raise serializers.ValidationError({
                    "invoice": "Payment cannot be created because this invoice is already marked as paid."
                })
            if PaymentInvoice.objects.filter(invoice=invoice).exists():
                raise serializers.ValidationError({
                    "invoice": "A payment record for this invoice already exists."
                })
            attrs['invoice'] = invoice
        else:  # Update operation
            if invoice_id is not None:
                # Disallow changing the related invoice on update.
                raise serializers.ValidationError({
                    "invoice_id": "Changing the associated invoice is not permitted."
                })
        return attrs

    def create(self, validated_data):
        """Create and return a new PaymentInvoice instance."""
        return PaymentInvoice.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update the entire PaymentInvoice model with provided data.
        
        Unlike the create method, here we allow updating any field on PaymentInvoice.
        (Note: Access control is assumed to be handled by a custom permission class.)
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
