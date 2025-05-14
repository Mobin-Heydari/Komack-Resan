from rest_framework import serializers

from .models import Service, ServiceEmployee
from Companies.models import Company, CompanyEmployee, CompanyCard
from Companies.serializers import CompanyCardSerializer
from Addresses.models import RecipientAddress

import uuid




class ServiceSerializer(serializers.ModelSerializer):
    # Read-only fields for display.
    company = serializers.SlugRelatedField(read_only=True, slug_field='name')
    service_provider = serializers.SlugRelatedField(read_only=True, slug_field='full_name')
    recepient = serializers.SlugRelatedField(read_only=True, slug_field='full_name')
    company_card = CompanyCardSerializer(read_only=True)
    
    # Computed human‐readable display fields.
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
    service_status_display = serializers.CharField(source='get_service_status_display', read_only=True)
    
    # Computed fields.
    overall_score = serializers.SerializerMethodField(read_only=True)
    time_elapsed = serializers.SerializerMethodField(read_only=True)
    
    # Write-only fields for assigning relations.
    company_slug = serializers.CharField(write_only=True, required=True)
    recipient_address_id = serializers.IntegerField(write_only=True, required=True)
    
    # New field to allow assignment of a company card (only by company.employer).
    company_card_id = serializers.IntegerField(write_only=True, required=False)
    
    # New fields for payment method.
    payment_method = serializers.ChoiceField(
        choices=Service.PaymentMethodChoices.choices, required=False
    )
    transaction_screenshot = serializers.ImageField(required=False, allow_null=True)
    
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
            "company_card_id",
            "company_card",
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
            "payment_method",
            "transaction_screenshot",
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
          • Use company_slug to fetch the Company and validate its status.
          • Ensure title and descriptions are provided.
          • Set recepient to the current user.
          • Lookup recipient address via recipient_address_id.
          • Generate a random slug using UUID4.
          • Disallow setting payment_status during creation.
        On update:
          • Disallow changes to company (via company_slug).
          • Only allow updating payment_status if request.user is the service_provider.
          • Only allow updating service_status if request.user is the recepient.
          • Allow updating recipient_address.
        Additionally:
          • Only a service recipient (user_type "SC") may choose the payment method.
          • When payment_method is set to "transaction" by a service recipient,
            the transaction_screenshot is not required immediately (can be provided later).
          • Only the company employer may add (or update) a company card to the service.
            If provided as company_card_id, the card's company must match the service's company.
        """
        request = self.context.get("request")
        user = request.user

        # Ensure required text fields are present.
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

            # Set service_provider to the company's employer.
            attrs["service_provider"] = company.employer

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

            # Do not allow setting payment_status during creation.
            if "payment_status" in attrs:
                raise serializers.ValidationError({"payment_status": "Not authorized to set payment status at creation."})

            # Generate a random slug.
            attrs["slug"] = str(uuid.uuid4())
        
        else:  # Update
            # Disallow changes to company.
            if "company_slug" in attrs:
                raise serializers.ValidationError({"company_slug": "Cannot change company."})
            # Only allow updating payment_status if request.user equals service_provider.
            if "payment_status" in attrs:
                if user != self.instance.service_provider:
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

            # Process company card update if provided.
            if "company_card_id" in attrs:
                card_id = attrs.pop("company_card_id")
                try:
                    company_card = CompanyCard.objects.get(id=card_id)
                except CompanyCard.DoesNotExist:
                    raise serializers.ValidationError({"company_card_id": "Company card not found."})
                # Ensure that the card belongs to the same company as the service.
                if company_card.company != self.instance.company:
                    raise serializers.ValidationError({
                        "company_card_id": "The provided company card does not belong to this service's company."
                    })
                # Ensure that only the company employer can update the company card.
                if self.instance.company.employer != user:
                    raise serializers.ValidationError({
                        "company_card_id": "Only the company employer is authorized to add or update the company card."
                    })
                attrs["company_card"] = company_card

            # --- Validation for payment method ---
            if "payment_method" in attrs:
                if getattr(user, 'user_type', None) != "SC":
                    raise serializers.ValidationError({
                        "payment_method": "Only the service recipient may choose the payment method."
                    })
                # When choosing "transaction", we relax the screenshot requirement.
        
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
    
    # Write-only fields for assigning related objects.
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
    
    def validate(self, attrs):
        """
        Enforces that:
          - On creation:
              * The service (looked up via 'recipient_service_slug') must exist.
              * The service must have its service_status either PENDING ('PE') or IN_PROGRESS ('IP').
              * The requesting user (from context) must equal service.service_provider.
              * The employee lookup (via employee_id) must succeed.
          - On update:
              * The fields 'recipient_service_slug' and 'employee_id' cannot be changed.
              * Additionally, the underlying service must remain in a PENDING or IN_PROGRESS state.
              * Also only the service provider can update.
        """
        request = self.context.get("request")
        user = request.user
        
        if not self.instance:  # Creation flow.
            # Look up the service via recipient_service_slug.
            service_slug = attrs.pop("recipient_service_slug")
            try:
                service = Service.objects.get(slug=service_slug)
            except Service.DoesNotExist:
                raise serializers.ValidationError({
                    "recipient_service_slug": "Service not found."
                })
            # Validate service status.
            if service.service_status not in [Service.ServiceStatusChoices.PENDING, Service.ServiceStatusChoices.IN_PROGRESS]:
                raise serializers.ValidationError({
                    "recipient_service_slug": "Employees can only be added to services in a PENDING or IN_PROGRESS state."
                })
            # Check that the requester is the service's provider.
            if user != service.service_provider:
                raise serializers.ValidationError({
                    "recipient_service_slug": "Only the service provider can add service employees."
                })
            attrs["recipient_service"] = service
            
            # Process employee lookup.
            employee_id = attrs.pop("employee_id")
            try:
                employee = CompanyEmployee.objects.get(id=employee_id)
            except CompanyEmployee.DoesNotExist:
                raise serializers.ValidationError({
                    "employee_id": "Employee not found."
                })
            attrs["employee"] = employee

        else:  # Update flow.
            if "recipient_service_slug" in attrs:
                raise serializers.ValidationError({
                    "recipient_service_slug": "Cannot change the service for a service employee."
                })
            if "employee_id" in attrs:
                raise serializers.ValidationError({
                    "employee_id": "Cannot change the employee for a service employee."
                })
            # Additionally, check that the service status is still valid.
            service = self.instance.recipient_service
            if service.service_status not in [Service.ServiceStatusChoices.PENDING, Service.ServiceStatusChoices.IN_PROGRESS]:
                raise serializers.ValidationError("Employees can only be managed for services in a PENDING or IN_PROGRESS state.")
            # And ensure only the service provider is allowed to perform updates.
            if user != service.service_provider:
                raise serializers.ValidationError("Only the service provider can manage service employees.")
        
        return attrs

    def create(self, validated_data):
        return ServiceEmployee.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        # For updates, the only fields that can be updated are those other than the service and employee; typically job_title.
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
