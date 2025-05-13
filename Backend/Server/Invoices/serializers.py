from django.utils import timezone
from datetime import timedelta

from rest_framework import serializers

from .models import InvoiceItem, Invoice
from Companies.models import Company
from Services.models import Service




class InvoiceItemSerializer(serializers.ModelSerializer):
    # Display the service title from the related Service.
    service = serializers.SlugRelatedField(read_only=True, slug_field='title')

    class Meta:
        model = InvoiceItem
        fields = [
            'service', 'amount', 'created_at',
        ]
        read_only_fields = fields



class InvoiceSerializer(serializers.ModelSerializer):
    # Write-only field for inputting company_slug.
    company_slug = serializers.CharField(write_only=True, required=True)
    # Nested, read-only representation of invoice items.
    items = InvoiceItemSerializer(many=True, read_only=True)
    # Display the company name for clarity.
    company = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = Invoice
        fields = [
            'company', 'company_slug', 'total_amount', 'is_paid', 'deadline', 'deadline_status',
            'created_at', 'updated_at', 'items',
        ]
        read_only_fields = ['company', 'created_at', 'updated_at']

    def validate(self, data):
        """
        Validate that a valid company_slug is provided.
        Looks up the company based on the provided slug and attaches the company instance
        to the validated data.
        """
        company_slug = data.get('company_slug')
        if not company_slug:
            raise serializers.ValidationError({"company_slug": "This field is required."})
        try:
            company = Company.objects.get(slug=company_slug)
        except Company.DoesNotExist:
            raise serializers.ValidationError({"company_slug": "No company exists with this slug."})
        # Attach the company instance to the validated data.
        data['company'] = company
        return data

    def create(self, validated_data):
        """
        Create an Invoice for a company with pending services.

        Process:
          1. Remove company_slug (it's not a model field).
          2. Use the provided company (populated during validation).
          3. Retrieve all Service objects for that Company where is_invoiced is False.
          4. Set a deadline 30 days from now.
          5. Create an Invoice and create an InvoiceItem for each pending service.
          6. Mark each service as invoiced.
          7. Calculate and update the total amount of the invoice.
        """
        # Remove company_slug as it is not part of the model.
        validated_data.pop('company_slug', None)
        company = validated_data.get('company')

        # Retrieve all pending services for this company.
        services = Service.objects.filter(company=company, is_invoiced=False)
        if not services.exists():
            raise serializers.ValidationError("No pending services available for invoicing.")

        # Set a deadline 30 days from now.
        deadline = timezone.now() + timedelta(days=30)

        # Create the Invoice instance.
        invoice = Invoice.objects.create(
            company=company,
            deadline=deadline
        )

        # For each pending service, create an InvoiceItem and mark the service as invoiced.
        for service in services:
            InvoiceItem.objects.create(
                invoice=invoice,
                service=service
            )
            service.is_invoiced = True
            service.save()

        # Calculate and update the invoice total (assuming your Invoice model has a method to do this).
        invoice.calculate_total()

        return invoice

    def update(self, instance, validated_data):
        """
        Update only the mutable fields.
        Permission checks are handled by dedicated permissions.
        """
        instance.total_amount = validated_data.get('total_amount', instance.total_amount)
        instance.is_paid = validated_data.get('is_paid', instance.is_paid)
        instance.deadline = validated_data.get('deadline', instance.deadline)
        instance.deadline_status = validated_data.get('deadline_status', instance.deadline_status)
        instance.save()
        return instance
