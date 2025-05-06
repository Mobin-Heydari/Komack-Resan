from rest_framework import serializers
from django.conf import settings
from .models import *



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


class CompanySerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    banner = serializers.SerializerMethodField()
    intro_video = serializers.SerializerMethodField()
    validation_status = CompanyValidationStatusSerializer(read_only=True)

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
