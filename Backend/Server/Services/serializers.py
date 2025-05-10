from rest_framework import serializers

from .models import Service, ServiceEmployee
from Companies.models import Company, CompanyEmployee
from Addresses.models import RecipientAddress



class ServiceSerializer(serializers.ModelSerializer):
    # Read-only display fields.
    company = serializers.SlugRelatedField(read_only=True, slug_field='name')
    service_provider = serializers.SlugRelatedField(read_only=True, slug_field='full_name')
    recepient = serializers.SlugRelatedField(read_only=True, slug_field='full_name')
    
    # Computed field for an overall score (if a score exists)
    overall_score = serializers.SerializerMethodField()
    # Display choices as human-readable fields.
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
    service_status_display = serializers.CharField(source='get_service_status_display', read_only=True)
    # Optionally, return time elapsed (in seconds) from start to finish.
    time_elapsed = serializers.SerializerMethodField()
    
    # Write-only fields for assigning related objects.
    company_slug = serializers.CharField(write_only=True, required=True)
    recipient_address_id = serializers.IntegerField(write_only=True, required=True)
    
    class Meta:
        model = Service
        fields = [
            "id",
            "company",
            "company_slug",
            "service_provider",
            "recepient",
            "recipient_address",
            "recipient_address_id",
            "title",
            "slug",
            "descriptions",
            "payment_status",
            "payment_status_display",
            "service_status",
            "service_status_display",
            "is_invoiced",
            "started_at",
            "finished_at",
            "created_at",
            "updated_at",
            "overall_score",
            "time_elapsed",
        ]
        read_only_fields = [
            "company", 
            "service_provider", 
            "recepient", 
            "is_invoiced", 
            "created_at", 
            "updated_at",
            "overall_score",
            "time_elapsed",
        ]
    
    def get_overall_score(self, obj):
        return obj.overall_score

    def get_time_elapsed(self, obj):
        if obj.started_at and obj.finished_at:
            return (obj.finished_at - obj.started_at).total_seconds()
        return None



class ServiceEmployeeSerializer(serializers.ModelSerializer):
    # Read-only fields for display.
    recipient_service = serializers.SlugRelatedField(read_only=True, slug_field='title')
    employee = serializers.SlugRelatedField(read_only=True, slug_field='employee__full_name')
    # Return the company name from the associated service.
    service_company = serializers.SerializerMethodField(read_only=True)
    
    # Write-only fields to assign related objects.
    recipient_service_slug = serializers.CharField(write_only=True, required=True)
    employee_id = serializers.IntegerField(write_only=True, required=True)
    
    class Meta:
        model = ServiceEmployee
        fields = [
            "id",
            "job_title",
            "recipient_service",
            "recipient_service_slug",
            "employee",
            "employee_id",
            "service_company",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "recipient_service", 
            "employee", 
            "created_at", 
            "updated_at", 
            "service_company",
        ]
    
    def get_service_company(self, obj):
        # Return the company name from the associated service.
        if obj.recipient_service and obj.recipient_service.company:
            return obj.recipient_service.company.name
        return None