from rest_framework import serializers
from .models import InvoiceItem, Invoice




class InvoiceItemSerializer(serializers.ModelSerializer):
    # Display the service title from the related Service
    service = serializers.SlugRelatedField(read_only=True, slug_field='title')
    
    class Meta:
        model = InvoiceItem
        fields = [
            'service',
            'amount',
            'created_at',
        ]
        read_only_fields = fields


class InvoiceSerializer(serializers.ModelSerializer):
    # Nested, read-only representation of invoice items.
    items = InvoiceItemSerializer(many=True, read_only=True)
    # Display the company name for clarity.
    company = serializers.SlugRelatedField(read_only=True, slug_field='name')
    
    class Meta:
        model = Invoice
        fields = [
            'company',
            'total_amount',
            'is_paid',
            'deadline',
            'deadline_status',
            'created_at',
            'updated_at',
            'items',
        ]
        read_only_fields = ['company', 'created_at', 'updated_at']
    
    def update(self, instance, validated_data):
        """
        Update only the mutable fields.
        Note: Permission checks are removed here and handled via
        a dedicated permissions file.
        """
        instance.total_amount = validated_data.get('total_amount', instance.total_amount)
        instance.is_paid = validated_data.get('is_paid', instance.is_paid)
        instance.deadline = validated_data.get('deadline', instance.deadline)
        instance.deadline_status = validated_data.get('deadline_status', instance.deadline_status)
        instance.save()
        return instance
