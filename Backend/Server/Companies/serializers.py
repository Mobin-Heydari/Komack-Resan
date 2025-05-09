from django.conf import settings
from django.db import transaction

from rest_framework import serializers

from .models import *

import datetime




def get_full_host():
    if not settings.ALLOWED_HOSTS:
        return "http://127.0.0.1:8000"
    return settings.ALLOWED_HOSTS[0]


class FirstItemSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()

    class Meta:
        model = FirstItem
        fields = "__all__"

    def get_icon(self, obj):
        if obj.icon:
            return f"{get_full_host()}{obj.icon.url}"
        return None
    

    def create(self, validated_data):
        # Generate a slug for the first_item based on its name.
        generated_slug = slugify(validated_data.get('name'), allow_unicode=True)
        validated_data['slug'] = generated_slug

        # Create the first_item and its related validation status atomically.
        with transaction.atomic():
            first_item = FirstItem.objects.create(**validated_data)
        
        return first_item
    

    def update(self, instance, validated_data):
        # Optionally, if the name is updated, regenerate the slug.
        if 'name' in validated_data:
            validated_data['slug'] = slugify(validated_data['name'], allow_unicode=True)

        # Update instance fields.
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
        



class SecondItemSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()

    class Meta:
        model = SecondItem
        fields = "__all__"
    
    def get_icon(self, obj):
        if obj.icon:
            return f"{get_full_host()}{obj.icon.url}"
        return None
    

    def create(self, validated_data):
        # Generate a slug for the second_item based on its name.
        generated_slug = slugify(validated_data.get('name'), allow_unicode=True)
        validated_data['slug'] = generated_slug

        # Create the second_item and its related validation status atomically.
        with transaction.atomic():
            second_item = SecondItem.objects.create(**validated_data)
        
        return second_item
    

    def update(self, instance, validated_data):
        # Optionally, if the name is updated, regenerate the slug.
        if 'name' in validated_data:
            validated_data['slug'] = slugify(validated_data['name'], allow_unicode=True)

        # Update instance fields.
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


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
    day_of_week_display = serializers.CharField(source='get_day_of_week_display', read_only=True)
    # Returns the working hours string, e.g., "09:00 - 17:00" or "Closed"
    time_range = serializers.SerializerMethodField()
    # Returns True if the company is open for this day at the current time; False otherwise.
    is_open_now = serializers.SerializerMethodField()

    class Meta:
        model = WorkDay
        fields = [
            'company',
            'day_of_week',
            'day_of_week_display',
            'open_time',
            'close_time',
            'is_closed',
            'time_range',
            'is_open_now'
        ]

    def get_time_range(self, obj):
        # Leverage the model’s time_range property
        return obj.time_range

    def get_is_open_now(self, obj):
        """
        Determines if the company is currently open for this workday.
        The method:
          1. Gets the current local time.
          2. Gets the current day name in lowercase.
          3. Checks if the current day matches the workday carried by this serializer record.
          4. If the day matches, and the workday isn’t marked as closed,
             it checks if the current time falls within the open and close times.
        """
        now = datetime.datetime.now().time()
        # Determine the current day (e.g., 'monday', 'tuesday', etc.)
        current_day = datetime.datetime.today().strftime('%A').lower()

        # If the workday does not correspond to today, it's not open now.
        if obj.day_of_week != current_day:
            return False

        # If the day is marked as closed, the company is closed.
        if obj.is_closed:
            return False

        # Check if open_time and close_time are provided and then whether the current time is within them.
        if obj.open_time and obj.close_time:
            if obj.open_time <= now <= obj.close_time:
                return True

        return False
    

class CompanyFirstItemSerializer(serializers.ModelSerializer):
    first_item = FirstItemSerializer(read_only=True)

    class Meta:
        model = CompanyFirstItem
        fields = "__all__"


# Nested serializer for the company's second item:
class CompanySecondItemSerializer(serializers.ModelSerializer):
    second_item = SecondItemSerializer(read_only=True)

    class Meta:
        model = CompanySecondItem
        fields = "__all__"

    
class CompanySerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    banner = serializers.SerializerMethodField()
    intro_video = serializers.SerializerMethodField()
    validation_status = CompanyValidationStatusSerializer(read_only=True)
    workdays = WorkDaySerializer(many=True, read_only=True)
    companies_first_item = CompanyFirstItemSerializer(many=True, read_only=True)
    companies_second_item = CompanySecondItemSerializer(many=True, read_only=True)
    # Use a write-only field for industry identification
    industry_slug = serializers.CharField(write_only=True, help_text="The slug representing the industry.")

    class Meta:
        model = Company
        fields = "__all__"
        read_only_fields = ('employer', 'industry')  # employer is set based on the request user

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
        request = self.context.get('request')
        employer = request.user if request else None

        # Prevent duplicate companies for the same employer.
        if employer and Company.objects.filter(employer=employer, name=attrs.get('name')).exists():
            raise serializers.ValidationError("A company with this name already exists for you.")
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        employer = request.user

        # Remove industry_slug and fetch the actual Industry instance
        industry_slug = validated_data.pop('industry_slug')
        industry = Industry.objects.get(slug=industry_slug)

        # Generate a slug for the company based on its name.
        generated_slug = slugify(validated_data.get('name'), allow_unicode=True)
        validated_data['slug'] = generated_slug

        # Force the is_validated field: only admin can set it.
        if not request.user.is_staff:
            # Owners (or any non-admins) cannot override is_validated at creation.
            validated_data['is_validated'] = False

        # Create the company and its related validation status atomically.
        with transaction.atomic():
            company = Company.objects.create(
                employer=employer,
                industry=industry,
                **validated_data
            )
            CompanyValidationStatus.objects.create(company=company)
        return company

    def update(self, instance, validated_data):
        request = self.context.get('request')

        # If industry_slug is provided, update the company’s industry.
        industry_slug = validated_data.pop('industry_slug', None)
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


class CompanyEmployeeSerializer(serializers.ModelSerializer):

    company = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    employee = serializers.SlugRelatedField(
        read_only=True,
        slug_field='full_name'
    )

    class Meta:
        model = CompanyEmployee
        fields = ['id', 'company', 'employee', 'position', 'created_at', 'updated_at']
        read_only_fields = ('company', 'employee', 'created_at')