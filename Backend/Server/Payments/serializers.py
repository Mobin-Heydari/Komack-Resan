from rest_framework import serializers
from .models import PaymentInvoice
from Invoices.models import Invoice
from Invoices.serializers import InvoiceSerializer  # Assuming this serializer exists for invoice details



class PaymentInvoiceSerializer(serializers.ModelSerializer):
    # Display nested invoice details on read.
    invoice = InvoiceSerializer(read_only=True)
    # For write operations, we accept the invoice's UUID as invoice_id.
    invoice_id = serializers.CharField(
        write_only=True,
        required=True,
        help_text="The UUID of the invoice for which this payment is made."
    )

    class Meta:
        model = PaymentInvoice
        fields = [
            'id',               # UUID primary key
            'invoice',          # Nested invoice details (read-only)
            'invoice_id',       # Write-only field for specifying the invoice
            'amount',
            'transaction_id',
            'payment_status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'invoice', 'created_at', 'updated_at']

    def validate(self, attrs):
        """
        Validate the following conditions on create:
          - An invoice_id is provided and the invoice exists.
          - The invoice is not already paid.
          - No PaymentInvoice record exists for that invoice.
          - The owner of invoice.company is the same as the requesting user.
        """
        request = self.context.get('request')
        invoice_id = self.initial_data.get('invoice_id')  # Using raw input data
        
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
                "invoice": "Payment cannot be created for an invoice that is already marked as paid."
            })
        
        if PaymentInvoice.objects.filter(invoice=invoice).exists():
            raise serializers.ValidationError({
                "invoice": "A payment record for this invoice already exists."
            })
        
        # Check that the requesting user is the employer of the invoice's company.
        if getattr(invoice.company, 'employer', None) != request.user:
            raise serializers.ValidationError({
                "invoice": "Only the employer of the invoice's company can create a payment for this invoice."
            })
        
        # Add the retrieved invoice to the validated data.
        attrs['invoice'] = invoice
        return attrs

    def create(self, validated_data):
        """Create and return a new PaymentInvoice instance."""
        return PaymentInvoice.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update the PaymentInvoice instance. Here, all fields (except the immutable ones) are
        updated directly. (Access control for update is assumed to be handled externally via permissions.)
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
