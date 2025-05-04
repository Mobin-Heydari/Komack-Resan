from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from .models import (
    ServiceProviderProfile,
    ServiceRecipientProfile,
    AdminProfile,
    SupportProfile
)



class ServiceProviderProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProviderProfile
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

    def validate(self, attrs):
        request = self.context.get("request")
        if not request:
            raise serializers.ValidationError("Request object is required in the context.")

        # When updating an instance, only the owner or an admin can update it.
        if self.instance and self.instance.user != request.user and not request.user.is_staff:
            raise PermissionDenied("You do not have permission to update this profile.")

        return attrs

    def update(self, instance, validated_data):
        # Since validations are handled in validate(), we simply update the instance.
        return super().update(instance, validated_data)


class ServiceRecipientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRecipientProfile
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

    def validate(self, attrs):
        request = self.context.get("request")
        if not request:
            raise serializers.ValidationError("Request object is required in the context.")

        if self.instance and self.instance.user != request.user and not request.user.is_staff:
            raise PermissionDenied("You do not have permission to update this profile.")

        return attrs

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

    def validate(self, attrs):
        request = self.context.get("request")
        if not request:
            raise serializers.ValidationError("Request object is required in the context.")

        if self.instance and self.instance.user != request.user and not request.user.is_staff:
            raise PermissionDenied("You do not have permission to update this profile.")

        return attrs

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class SupportProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportProfile
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

    def validate(self, attrs):
        request = self.context.get("request")
        if not request:
            raise serializers.ValidationError("Request object is required in the context.")

        if self.instance and self.instance.user != request.user and not request.user.is_staff:
            raise PermissionDenied("You do not have permission to update this profile.")

        return attrs

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
