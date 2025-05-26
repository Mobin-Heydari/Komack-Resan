from django.conf import settings
from django.db import transaction

from rest_framework import serializers

from .models import FirstItem, SecondItem



def get_full_host():
    if not settings.ALLOWED_HOSTS:
        return "http://127.0.0.1:8000"
    return settings.ALLOWED_HOSTS[0]



class FirstItemSerializer(serializers.ModelSerializer):
    # This field is used for output
    icon_url = serializers.SerializerMethodField()
    # Use this field for write operations
    icon = serializers.ImageField(write_only=True, required=False)
    name = serializers.CharField(required=False)
    slug = serializers.CharField(required=False)

    class Meta:
        model = FirstItem
        fields = ['name', 'icon_url', 'icon', 'slug']
    
    def get_icon_url(self, obj):
        if obj.icon:
            return f"{get_full_host()}{obj.icon.url}"
        return None

    def create(self, validated_data):
        # Create the first_item atomically.
        with transaction.atomic():
            first_item = FirstItem.objects.create(**validated_data)
        return first_item

    def update(self, instance, validated_data):
        # Update the instance with new data if provided.
        instance.name = validated_data.get('name', instance.name)
        # Only update the icon if new data is provided.
        if 'icon' in validated_data:
            instance.icon = validated_data.get('icon')
        instance.slug = validated_data.get('slug', instance.slug)

        instance.save()
        return instance

        

class SecondItemSerializer(serializers.ModelSerializer):
    # This field is used for output
    icon_url = serializers.SerializerMethodField()
    # Use this field for write operations
    icon = serializers.ImageField(write_only=True, required=False)
    name = serializers.CharField(required=False)
    slug = serializers.CharField(required=False)

    class Meta:
        model = SecondItem
        fields = ['name', 'icon_url', 'icon', 'slug']
    
    def get_icon_url(self, obj):
        if obj.icon:
            return f"{get_full_host()}{obj.icon.url}"
        return None

    def create(self, validated_data):
        # Create the first_item atomically.
        with transaction.atomic():
            first_item = SecondItem.objects.create(**validated_data)
        return first_item

    def update(self, instance, validated_data):
        # Update the instance with new data if provided.
        instance.name = validated_data.get('name', instance.name)
        # Only update the icon if new data is provided.
        if 'icon' in validated_data:
            instance.icon = validated_data.get('icon')
        instance.slug = validated_data.get('slug', instance.slug)

        instance.save()
        return instance

