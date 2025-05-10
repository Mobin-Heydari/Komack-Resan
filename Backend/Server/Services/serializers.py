from rest_framework import serializers

from .models import Service, ServiceEmployee
from Companies.models import Company, CompanyEmployee
from Addresses.models import RecipientAddress

import uuid


class ServiceSerializer(serializers.ModelSerializer):
    # Read-only fields for display.
    company = serializers.SlugRelatedField(read_only=True, slug_field='name')
    service_provider = serializers.SlugRelatedField(read_only=True, slug_field='full_name')
    recepient = serializers.SlugRelatedField(read_only=True, slug_field='full_name')
    
    # Computed human‐readable display fields.
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
    service_status_display = serializers.CharField(source='get_service_status_display', read_only=True)
    
    # Computed fields.
    overall_score = serializers.SerializerMethodField(read_only=True)
    time_elapsed = serializers.SerializerMethodField(read_only=True)
    
    # Write-only fields for assigning relations.
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
            "recipient_address", 
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

    def validate(self, attrs):
        """
        On creation:
          • Use the provided company_slug to fetch the Company and validate that it’s open.
          • Ensure title and descriptions are provided.
          • Set the recepient automatically to the current user.
          • Lookup the recipient address via recipient_address_id.
          • Generate a random slug using UUID4.
          • Disallow setting payment_status since only a service provider (or company owner) may do so.
        On update:
          • Disallow changes to company (via company_slug).
          • Only allow updating payment_status if the request.user is the service provider (or company owner).
          • Only allow updating service_status if the request.user is the recipient.
          • Allow updating the recipient address.
        """
        request = self.context.get("request")
        user = request.user

        # Ensure title and descriptions are present.
        if not attrs.get("title"):
            raise serializers.ValidationError({"title": "Title is required."})
        if not attrs.get("descriptions"):
            raise serializers.ValidationError({"descriptions": "Description is required."})
        
        if not self.instance:  # Creation
            # Process company_slug.
            company_slug = attrs.pop("company_slug", None)
            if not company_slug:
                raise serializers.ValidationError({"company_slug": "Company slug is required."})
            try:
                company = Company.objects.get(slug=company_slug)
            except Company.DoesNotExist:
                raise serializers.ValidationError({"company_slug": "Company not found."})
            # Validate company status.
            if not company.is_validated:
                raise serializers.ValidationError({"company": "The company is not validated."})
            if getattr(company, "is_off_season", False):
                raise serializers.ValidationError({"company": "The company is currently off season."})
            attrs["company"] = company

            # Set recepient to current user.
            attrs["recepient"] = user

            # Validate and assign recipient address.
            recipient_address_id = attrs.pop("recipient_address_id", None)
            if not recipient_address_id:
                raise serializers.ValidationError({"recipient_address_id": "Recipient address id is required."})
            try:
                recipient_address = RecipientAddress.objects.get(id=recipient_address_id)
            except RecipientAddress.DoesNotExist:
                raise serializers.ValidationError({"recipient_address_id": "Recipient address not found."})
            attrs["recipient_address"] = recipient_address

            # Do not allow setting payment_status during creation by a recipient.
            if "payment_status" in attrs:
                raise serializers.ValidationError({"payment_status": "Not authorized to set payment status at creation."})

            # Generate a random slug using uuid4.
            attrs["slug"] = str(uuid.uuid4())
        
        else:  # Update
            # Disallow changes to company.
            if "company_slug" in attrs:
                raise serializers.ValidationError({"company_slug": "Cannot change company."})
            # Only allow updating payment_status if request.user equals service_provider.
            if "payment_status" in attrs:
                if user != self.instance.service_provider:
                    # Optionally, if your Company model has an owner field, you may also check:
                    # if not hasattr(self.instance.company, "owner") or user != self.instance.company.owner:
                    raise serializers.ValidationError({"payment_status": "Not authorized to update payment status."})
            # Only allow updating service_status if request.user is the recepient.
            if "service_status" in attrs:
                if user != self.instance.recepient:
                    raise serializers.ValidationError({"service_status": "Only the recipient can update service status."})
            # Process recipient_address update if provided.
            if "recipient_address_id" in attrs:
                recipient_address_id = attrs.pop("recipient_address_id")
                try:
                    recipient_address = RecipientAddress.objects.get(id=recipient_address_id)
                except RecipientAddress.DoesNotExist:
                    raise serializers.ValidationError({"recipient_address_id": "Recipient address not found."})
                attrs["recipient_address"] = recipient_address
        
        return attrs

    def create(self, validated_data):
        # Create the Service instance using the validated data.
        instance = Service.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        # Update allowed fields.
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance



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