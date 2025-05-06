from django.conf import settings

from rest_framework import serializers

from .models import *

import datetime




def get_full_host():
    if not settings.ALLOWED_HOSTS:
        return "http://127.0.0.1:8000"
    return settings.ALLOWED_HOSTS[0]


class FirstItemSerializers(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()

    class Meta:
        model = FirstItem
        fields = "__all__"

    def get_icon(self, obj):
        if obj.icon:
            return f"{get_full_host()}{obj.icon.url}"
        return None


class SecondItemSerializers(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()

    class Meta:
        model = SecondItem
        fields = "__all__"
    
    def get_icon(self, obj):
        if obj.icon:
            return f"{get_full_host()}{obj.icon.url}"
        return None


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

    
class CompanySerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    banner = serializers.SerializerMethodField()
    intro_video = serializers.SerializerMethodField()
    validation_status = CompanyValidationStatusSerializer(read_only=True)
    # Include workdays as a nested representation.
    workdays = WorkDaySerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = "__all__"
        read_only_fields = ('employer',)

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