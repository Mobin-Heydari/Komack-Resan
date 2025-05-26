from django.conf import settings
from django.db import transaction

from rest_framework import serializers

from .models import *

from Addresses.serializers import CitySerializer, ProvinceSerializer
from Items.serializers import FirstItemSerializer, SecondItemSerializer

import datetime




def get_full_host():
    if not settings.ALLOWED_HOSTS:
        return "http://127.0.0.1:8000"
    return settings.ALLOWED_HOSTS[0]


class CompanyValidationStatusSerializer(serializers.ModelSerializer):
    validated_by = serializers.SerializerMethodField()

    class Meta:
        model = CompanyValidationStatus
        fields = "__all__"

    def get_validated_by(self, obj):
        # Ensure the validated_by user exists and return full_name if available.
        if obj.validated_by:
            return getattr(obj.validated_by, "full_name", str(obj.validated_by))
        return None
    

    def update(self, instance, validated_data):
        request = self.context.get('request')
        
        if request.user.is_staff:
            # Admin branch: update overall_status and related fields.
            overall_status = validated_data.get('overall_status', instance.overall_status)

            if overall_status == CompanyValidationStatus.ValidationStatus.APPROVED:
                instance.validated_by = request.user
                # Use the model's method to mark as validated.
                instance.mark_as_validated()
                # Update the associated company as validated.
                company = instance.company
                company.is_validated = True
                company.save()

            elif overall_status == CompanyValidationStatus.ValidationStatus.REJECTED:
                if not validated_data.get('validation_notes'):
                    raise serializers.ValidationError(
                        "Validation notes must be provided when rejecting a company."
                    )
                instance.overall_status = overall_status
                # Mark the company as not validated.
                company = instance.company
                company.is_validated = False
                company.save()

            else:
                # For pending or other statuses, update the overall_status directly.
                instance.overall_status = overall_status

            # Admins can update these fields.
            instance.business_license = validated_data.get(
                'business_license', instance.business_license
            )
            instance.business_license_status = validated_data.get(
                'business_license_status', instance.business_license_status
            )
            instance.validation_notes = validated_data.get(
                'validation_notes', instance.validation_notes
            )
            instance.save()
            return instance
        
        else:
            # Non-admin (company owner) branch.
            # Enforce that only the company employer can update the business license.
            if request.user != instance.company.employer:
                raise serializers.ValidationError("Only the company employer can update the business license.")
            
            # Allow update only when overall_status is either pending or rejected.
            allowed_statuses = [
                CompanyValidationStatus.ValidationStatus.PENDING,
                CompanyValidationStatus.ValidationStatus.REJECTED,
            ]
            if instance.overall_status not in allowed_statuses:
                raise serializers.ValidationError("You may update the business license only if the status is Pending or Rejected.")

            # Prevent any update to forbidden fields.
            forbidden_fields = ['overall_status', 'business_license_status', 'validation_notes']
            for field in forbidden_fields:
                if field in validated_data:
                    raise serializers.ValidationError({field: "You are not authorized to update this field."})
            
            # Allow the employer to update the business_license.
            if 'business_license' in validated_data:
                instance.business_license = validated_data['business_license']
            
            instance.save()
            return instance



class WorkDaySerializer(serializers.ModelSerializer):
    # Returns the human-readable day-of-week (e.g., "دوشنبه")
    day_of_week_display = serializers.CharField(source="get_day_of_week_display", read_only=True)
    # Returns the working hours string using the model’s time_range property.
    time_range = serializers.SerializerMethodField()
    # Returns True if the workday is currently active for the company.
    is_open_now = serializers.SerializerMethodField()
    # Accept the company slug (write-only) to identify the company during creation.
    company_slug = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = WorkDay
        fields = [
            "company",
            "company_slug",
            "day_of_week",
            "day_of_week_display",
            "open_time",
            "close_time",
            "is_closed",
            "time_range",
            "is_open_now",
        ]
        read_only_fields = ("company",)

    def get_time_range(self, obj):
        return obj.time_range

    def get_is_open_now(self, obj):
        now = datetime.datetime.now().time()
        current_day = datetime.datetime.today().strftime("%A").lower()
        if obj.day_of_week != current_day:
            return False
        if obj.is_closed:
            return False
        if obj.open_time and obj.close_time and (obj.open_time <= now <= obj.close_time):
            return True
        return False

    def validate(self, attrs):
        """
        For create: Remove company_slug and fetch the actual Company instance.
        For update: Prevent changing company by comparing provided slug with the current company.
        Also, enforce uniqueness of (company, day_of_week) across records.
        """
        # Creation
        if not self.instance:
            # Get company_slug from validated_data.
            company_slug = attrs.pop("company_slug")
            try:
                company = Company.objects.get(slug=company_slug)
            except Company.DoesNotExist:
                raise serializers.ValidationError({
                    "company_slug": "No company with this slug exists."
                })
            attrs["company"] = company
        else:
            # Update: Company cannot change.
            if "company_slug" in attrs:
                if attrs["company_slug"] != self.instance.company.slug:
                    raise serializers.ValidationError({
                        "company_slug": "Company cannot be changed on update."
                    })
            attrs["company"] = self.instance.company

        # Ensure that only one WorkDay exists for the given company and day_of_week.
        company = attrs["company"]
        # Use provided day_of_week (or fall back to the instance value during update).
        day_of_week = attrs.get("day_of_week", self.instance.day_of_week if self.instance else None)
        if not self.instance:
            if WorkDay.objects.filter(company=company, day_of_week=day_of_week).exists():
                raise serializers.ValidationError({
                    "day_of_week": "A workday for this day and company already exists."
                })
        else:
            qs = WorkDay.objects.filter(company=company, day_of_week=day_of_week).exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError({
                    "day_of_week": "A workday for this day and company already exists."
                })

        return attrs

    def create(self, validated_data):
        """
        Create a new WorkDay instance.
        The structure is similar to the industry example:
          - Remove company_slug (already popped in validation) and fetch the actual Company instance.
          - Run model-level validations via full_clean().
        """
        with transaction.atomic():
            instance = WorkDay(**validated_data)
            instance.full_clean()
            instance.save()
        return instance

    def update(self, instance, validated_data):
        """
        Update the WorkDay instance. Disallows changes to the company.
        """
        # Remove company_slug if present.
        validated_data.pop("company_slug", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.full_clean()
        instance.save()
        return instance



class CompanyFirstItemSerializer(serializers.ModelSerializer):
    # Read-only nested representation for display.
    first_item = FirstItemSerializer(read_only=True)
    # Write-only field expecting the first_item slug.
    first_item_slug = serializers.CharField(write_only=True)
    # Write-only field to supply the company slug.
    company_slug = serializers.CharField(write_only=True)

    class Meta:
        model = CompanyFirstItem
        fields = "__all__"
        # The company association field (named “compay” in your model) remains read-only.
        read_only_fields = ('compay',)

    def validate(self, attrs):
        # Validate the provided company_slug.
        company_slug = attrs.get('company_slug')
        try:
            company = Company.objects.get(slug=company_slug)
        except Company.DoesNotExist:
            raise serializers.ValidationError({
                "company_slug": "Company with the provided slug does not exist."
            })
        # Save the company instance under the model field name.
        attrs['compay'] = company

        # Validate the provided first_item_slug.
        first_item_slug = attrs.get('first_item_slug')
        try:
            first_item = FirstItem.objects.get(slug=first_item_slug)
        except FirstItem.DoesNotExist:
            raise serializers.ValidationError({
                "first_item_slug": "First item with the provided slug does not exist."
            })
        attrs['first_item'] = first_item

        return attrs

    def create(self, validated_data):
        # Remove write-only slug fields.
        validated_data.pop('company_slug', None)
        validated_data.pop('first_item_slug', None)
        with transaction.atomic():
            instance = CompanyFirstItem.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        # Remove the write-only slug fields before updating.
        validated_data.pop('company_slug', None)
        validated_data.pop('first_item_slug', None)
        # Allow updating the first_item if provided.
        if 'first_item' in validated_data:
            instance.first_item = validated_data['first_item']
        instance.save()
        return instance



class CompanySecondItemSerializer(serializers.ModelSerializer):
    # Read-only nested representation for display.
    second_item = SecondItemSerializer(read_only=True)
    # Write-only field for the second_item slug.
    second_item_slug = serializers.CharField(write_only=True)
    # Write-only field for the company slug.
    company_slug = serializers.CharField(write_only=True)

    class Meta:
        model = CompanySecondItem
        fields = "__all__"
        # The company association (named 'compay' in your model) is read-only.
        read_only_fields = ('compay',)

    def validate(self, attrs):
        # Validate the provided company_slug.
        company_slug = attrs.get('company_slug')
        try:
            company = Company.objects.get(slug=company_slug)
        except Company.DoesNotExist:
            raise serializers.ValidationError({
                "company_slug": "Company with the provided slug does not exist."
            })
        attrs['compay'] = company

        # Validate the provided second_item_slug.
        second_item_slug = attrs.get('second_item_slug')
        try:
            second_item = SecondItem.objects.get(slug=second_item_slug)
        except SecondItem.DoesNotExist:
            raise serializers.ValidationError({
                "second_item_slug": "Second item with the provided slug does not exist."
            })
        attrs['second_item'] = second_item

        return attrs

    def create(self, validated_data):
        validated_data.pop('company_slug', None)
        validated_data.pop('second_item_slug', None)
        with transaction.atomic():
            instance = CompanySecondItem.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        validated_data.pop('company_slug', None)
        validated_data.pop('second_item_slug', None)
        # Allow updating the second_item if provided.
        if 'second_item' in validated_data:
            instance.second_item = validated_data['second_item']
        instance.save()
        return instance
    



class CompanySerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(required=False)
    banner = serializers.ImageField(required=False)
    intro_video = serializers.FileField(required=False)
    validation_status = CompanyValidationStatusSerializer(read_only=True)
    workdays = WorkDaySerializer(many=True, read_only=True)
    companies_first_item = CompanyFirstItemSerializer(many=True, read_only=True)
    companies_second_item = CompanySecondItemSerializer(many=True, read_only=True)
    city = CitySerializer(read_only=True)
    province = ProvinceSerializer(read_only=True)
    # Use a write-only field for industry identification.
    industry_slug = serializers.CharField(
        write_only=True, help_text="The slug representing the industry.", required=False
    )
    # NEW write-only fields for location.
    city_slug = serializers.CharField(
        write_only=True, help_text="The slug representing the city.", required=False
    )
    province_slug = serializers.CharField(
        write_only=True, help_text="The slug representing the province.", required=False
    )
    name = serializers.CharField(required=False)
    
    class Meta:
        model = Company
        fields = "__all__"
        read_only_fields = ('employer', 'industry')
    
    def get_logo(self, obj):
        if obj.logo:
            return f"{get_full_host()}{obj.logo.url}"
        return None

    def get_banner(self, obj):
        if obj.banner:
            return f"{get_full_host()}{obj.banner.url}"
        return None

    def get_intro_video(self, obj):
        if obj.intro_video:
            return f"{get_full_host()}{obj.intro_video.url}"
        return None

    def validate_industry_slug(self, value):
        """Ensure that the provided industry exists."""
        if not Industry.objects.filter(slug=value).exists():
            raise serializers.ValidationError("The specified industry does not exist.")
        return value

    def validate(self, attrs):
        """
        In addition to the existing duplicate company check, process the location data.
        
        • On creation:
            - Prevent duplicate companies for the same employer.
            - If either city_slug or province_slug is provided, require both.
            - Look up the corresponding City and Province objects.
            - Validate that the city belongs to the province.
            - Assign the objects to the validated data.
        • On update:
            - If location update is requested (i.e. either city_slug or province_slug is in the input),
              require both fields and perform the same validations.
        """
        request = self.context.get('request')
        employer = request.user if request else None

        # For creation only: prevent duplicates.
        if not self.instance:
            if employer and Company.objects.filter(employer=employer, name=attrs.get('name')).exists():
                raise serializers.ValidationError("A company with this name already exists for you.")
        
        # Process location update if provided.
        city_slug = attrs.pop("city_slug", None)
        province_slug = attrs.pop("province_slug", None)
        
        # If one is provided, both must be.
        if (city_slug or province_slug):
            if not (city_slug and province_slug):
                raise serializers.ValidationError({
                    "city_slug": "Both city_slug and province_slug are required for location.",
                    "province_slug": "Both city_slug and province_slug are required for location."
                })
            # Look up the province.
            try:
                province = Province.objects.get(slug=province_slug)
            except Province.DoesNotExist:
                raise serializers.ValidationError({"province_slug": "Province not found."})
            # Look up the city.
            try:
                city = City.objects.get(slug=city_slug)
            except City.DoesNotExist:
                raise serializers.ValidationError({"city_slug": "City not found."})
            # Validate that the city belongs to the province.
            if city.province != province:
                raise serializers.ValidationError({
                    "city_slug": "The specified city is not located within the provided province."
                })
            # Attach the instances to validated data.
            attrs["city"] = city
            attrs["province"] = province
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        employer = request.user
        # Remove industry_slug and fetch the actual Industry instance if provided.
        industry_slug = validated_data.pop('industry_slug', None)
        if industry_slug:
            industry = Industry.objects.get(slug=industry_slug)
            validated_data['industry'] = industry
        # Generate a slug for the company based on its name.
        generated_slug = slugify(validated_data.get('name'), allow_unicode=True)
        validated_data['slug'] = generated_slug
        # Force the is_validated field: only admin can set it.
        if not request.user.is_staff:
            # Owners (or any non-admins) cannot override is_validated at creation.
            validated_data['is_validated'] = False
        # Set the employer based on the request user.
        with transaction.atomic():
            company = Company.objects.create(
                employer=employer,
                **validated_data
            )
            CompanyValidationStatus.objects.create(company=company)
        return company

    def update(self, instance, validated_data):
        request = self.context.get('request')
        # If industry_slug is provided, update the company’s industry.
        industry_slug = validated_data.get('industry_slug', None)
        if industry_slug:
            industry = Industry.objects.get(slug=industry_slug)
            validated_data['industry'] = industry
        # Prevent non-admin users from updating the is_validated field.
        if not request.user.is_staff and 'is_validated' in validated_data:
            validated_data.pop('is_validated')
        # Optionally, if the name is updated, regenerate the slug.
        if 'name' in validated_data:
            validated_data['slug'] = slugify(validated_data['name'], allow_unicode=True)
        # Update instance fields.
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance



class CompanyCardSerializer(serializers.ModelSerializer):
    # Display the company name in read-only mode.
    company = serializers.SlugRelatedField(read_only=True, slug_field='name')
    # Write-only field to lookup the company via its slug.
    company_slug = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = CompanyCard
        fields = [
            "id",
            "company",
            "company_slug",
            "card_number",
            "expiration_date",
            "card_holder_name",
            "created_at",
            "updated_at"
        ]
        read_only_fields = [
            "id", "company", "created_at", "updated_at"
        ]
    
    def validate(self, attrs):
        """
        Validate that a valid company_slug is provided and attach
        the corresponding Company object to the validated data.
        """
        company_slug = attrs.pop("company_slug", None)
        if company_slug is not None:
            try:
                company = Company.objects.get(slug=company_slug)
            except Company.DoesNotExist:
                raise serializers.ValidationError({"company_slug": "Invalid company slug."})
            attrs["company"] = company
            return attrs
        return attrs
        

    def create(self, validated_data):
        """
        Create a CompanyCard instance after
         ensuring that the requesting user is either an admin or the company's employer.
        """
        return CompanyCard.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update the CompanyCard instance after ensuring that only an admin or
         the company’s employer is authorized to modify the card details.
        """
        instance.card_number = validated_data.get("card_number", instance.card_number)
        instance.expiration_date = validated_data.get("expiration_date", instance.expiration_date)
        instance.card_holder_name = validated_data.get("card_holder_name", instance.card_holder_name)
        instance.save()
        return instance
