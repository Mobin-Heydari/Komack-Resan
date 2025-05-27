import uuid
from rest_framework import serializers
from .models import Service, ServicePayment
from Companies.models import Company, CompanyCard, CompanyReceptionist, CompanyAccountant, CompanyExpert
from Companies.serializers import CompanyCardSerializer
from Addresses.models import RecipientAddress




class ServiceSerializer(serializers.ModelSerializer):
    # Read-only fields for display
    company = serializers.SlugRelatedField(read_only=True, slug_field='name')
    service_provider = serializers.SlugRelatedField(read_only=True, slug_field='full_name')
    recipient = serializers.SlugRelatedField(read_only=True, slug_field='full_name')
    company_card = CompanyCardSerializer(read_only=True)
    
    # Computed display fields
    service_status_display = serializers.CharField(source='get_service_status_display', read_only=True)
    overall_score = serializers.SerializerMethodField(read_only=True)
    time_elapsed = serializers.SerializerMethodField(read_only=True)
    
    # Write-only helper fields for lookups
    company_slug = serializers.CharField(write_only=True, required=True)
    recipient_address_id = serializers.IntegerField(write_only=True, required=True)
    # PAYMENT fields have been removed from this serializer.
    
    class Meta:
        model = Service
        fields = [
            "id",
            "company",
            "company_slug",
            "service_provider",
            "recipient",
            "recipient_address",
            "recipient_address_id",
            "company_card",
            "title",
            "phone",
            "descriptions",
            "image",
            "service_status",
            "service_status_display",
            "service_type",
            "is_invoiced",
            "is_validated_by_receptionist",
            "first_item",
            "second_item",
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
            "recipient",
            "recipient_address",
            "is_invoiced",
            "created_at",
            "updated_at",
            "overall_score",
            "time_elapsed",
            "company_card",
        ]
    
    def get_overall_score(self, obj):
        return obj.overall_score

    def get_time_elapsed(self, obj):
        if obj.started_at and obj.finished_at:
            return (obj.finished_at - obj.started_at).total_seconds()
        return None

    def create(self, validated_data):
        """
        CREATE:
          - Use company_slug to look up and validate the Company.
          - Assign the company's employer as service_provider.
          - Look up the RecipientAddress using recipient_address_id.
          - Set the current user as the recipient.
          - (No need for slug handling as the id is an auto-generated UUID.)
        """
        request = self.context.get("request")
        user = request.user

        if not validated_data.get("title"):
            raise serializers.ValidationError({"title": "Title is required."})
        if not validated_data.get("descriptions"):
            raise serializers.ValidationError({"descriptions": "Description is required."})
        
        # Lookup Company
        company_slug = validated_data.pop("company_slug", None)
        if not company_slug:
            raise serializers.ValidationError({"company_slug": "Company slug is required."})
        try:
            company = Company.objects.get(slug=company_slug)
        except Company.DoesNotExist:
            raise serializers.ValidationError({"company_slug": "Company not found."})
        if not company.is_validated:
            raise serializers.ValidationError({"company": "The company is not validated."})
        if getattr(company, "is_off_season", False):
            raise serializers.ValidationError({"company": "The company is currently off season."})
        validated_data["company"] = company

        # Set service_provider & recipient
        validated_data["service_provider"] = company.employer
        validated_data["recipient"] = user

        # Lookup RecipientAddress
        recipient_address_id = validated_data.pop("recipient_address_id", None)
        if not recipient_address_id:
            raise serializers.ValidationError({"recipient_address_id": "Recipient address id is required."})
        try:
            recipient_address = RecipientAddress.objects.get(id=recipient_address_id)
        except RecipientAddress.DoesNotExist:
            raise serializers.ValidationError({"recipient_address_id": "Recipient address not found."})
        validated_data["recipient_address"] = recipient_address

        instance = Service.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        """
        UPDATE (Traditional structure without an allowed_fields set):
        
        * If the current user is the service recipient (creator), update basic fields:
            title, phone, descriptions, image, first_item, second_item, service_type.
        * If the current user is a receptionist – either the one already assigned OR if a
          CompanyReceptionist exists for the service's company with the current user – update:
            is_validated_by_receptionist, service_status, and receptionist if provided.
        * If the current user is an accountant (either already assigned or found in CompanyAccountant
          for the service's company), update the accountant field.
        * If the current user is an expert (either already assigned or found in CompanyExpert for the service's
          company), update the expert field and (if provided) service_status.
        * Always update the recipient_address if provided.
        """
        request = self.context.get("request")
        user = request.user

        # Service recipient updates (creator)
        if instance.recipient == user:
            if "title" in validated_data:
                instance.title = validated_data["title"]
            if "phone" in validated_data:
                instance.phone = validated_data["phone"]
            if "descriptions" in validated_data:
                instance.descriptions = validated_data["descriptions"]
            if "image" in validated_data:
                instance.image = validated_data["image"]
            if "first_item" in validated_data:
                instance.first_item = validated_data["first_item"]
            if "second_item" in validated_data:
                instance.second_item = validated_data["second_item"]
            if "service_type" in validated_data:
                instance.service_type = validated_data["service_type"]

        # Receptionist role (either already assigned or exists for the company with current user)
        if instance.receptionist or CompanyReceptionist.objects.filter(company=instance.company, employee=user).exists():
            if "is_validated_by_receptionist" in validated_data:
                instance.is_validated_by_receptionist = validated_data["is_validated_by_receptionist"]
            if "service_status" in validated_data:
                instance.service_status = validated_data["service_status"]
            if "receptionist" in validated_data:
                instance.receptionist = validated_data["receptionist"]

        # Accountant role – update accountant field if allowed.
        if instance.accountant or CompanyAccountant.objects.filter(company=instance.company, employee=user).exists():
            if "accountant" in validated_data:
                instance.accountant = validated_data["accountant"]

        # Expert role – update expert field and service_status if provided.
        if instance.expert or CompanyExpert.objects.filter(company=instance.company, employee=user).exists():
            if "expert" in validated_data:
                instance.expert = validated_data["expert"]
            if "service_status" in validated_data:
                instance.service_status = validated_data["service_status"]

        # Always update recipient_address if provided.
        if "recipient_address" in validated_data:
            instance.recipient_address = validated_data["recipient_address"]

        instance.save()
        return instance



class ServicePaymentSerializer(serializers.ModelSerializer):
    # Write-only field to assign a company card via its ID.
    company_card_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = ServicePayment
        fields = [
            "id",
            "service",
            "price",
            "company_card",
            "company_card_id",
            "payment_status",
            "payment_method",
            "transaction_screenshot",
            "paied_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id", "service", "paied_at", "created_at", "updated_at", "company_card"
        ]
    
    def validate_company_card_id(self, value):
        """
        Ensure the provided company card exists and, if updating, belongs
        to the same company as the related service.
        """
        try:
            card = CompanyCard.objects.get(id=value)
        except CompanyCard.DoesNotExist:
            raise serializers.ValidationError("Company card not found.")
        if self.instance:
            if card.company != self.instance.service.company:
                raise serializers.ValidationError(
                    "The provided company card does not belong to the service's company."
                )
        return value

    def update(self, instance, validated_data):
        request = self.context.get("request")
        user = request.user
        service = instance.service

        # Traditional update structure with role checks:
        # Admin users can update all fields.
        if user.is_staff:
            if "company_card_id" in validated_data:
                card_id = validated_data.pop("company_card_id")
                try:
                    card = CompanyCard.objects.get(id=card_id)
                except CompanyCard.DoesNotExist:
                    raise serializers.ValidationError({"company_card_id": "Company card not found."})
                if card.company != service.company:
                    raise serializers.ValidationError({
                        "company_card_id": "The provided company card does not belong to the service's company."
                    })
                instance.company_card = card
            instance.price = validated_data.get("price", instance.price)
            instance.payment_status = validated_data.get("payment_status", instance.payment_status)
            instance.payment_method = validated_data.get("payment_method", instance.payment_method)
            instance.transaction_screenshot = validated_data.get("transaction_screenshot", instance.transaction_screenshot)
            instance.save()
            return instance

        # If the user is the service recipient, allow only updating transaction_screenshot and payment_method.
        elif service.recipient == user:
            if "transaction_screenshot" in validated_data:
                instance.transaction_screenshot = validated_data["transaction_screenshot"]
            if "payment_method" in validated_data:
                instance.payment_method = validated_data["payment_method"]
            instance.save()
            return instance

        # If the user is the service accountant, allow updating price, payment_status, or company_card.
        elif service.accountant == user:
            if "price" in validated_data:
                instance.price = validated_data["price"]
            if "payment_status" in validated_data:
                instance.payment_status = validated_data["payment_status"]
            if "company_card_id" in validated_data:
                card_id = validated_data["company_card_id"]
                try:
                    card = CompanyCard.objects.get(company=service.company, id=card_id)
                except CompanyCard.DoesNotExist:
                    raise serializers.ValidationError({"company_card_id": "Company card not found."})
                if card.company != service.company:
                    raise serializers.ValidationError({
                        "company_card_id": "The provided company card does not belong to the service's company."
                    })
                instance.company_card = card
            instance.save()
            return instance

        # Otherwise, the user is not authorized to update.
        else:
            raise serializers.ValidationError("You are not authorized to update this payment.")
