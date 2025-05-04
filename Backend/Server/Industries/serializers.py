from rest_framework import serializers
from rest_framework.validators import ValidationError

from .models import IndustryCategory, Industry




class IndustryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustryCategory
        fields = '__all__'
        read_only_fields = ('slug',)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class IndustrySerializer(serializers.ModelSerializer):
    category = IndustryCategorySerializer(read_only=True)

    class Meta:
        model = Industry
        fields = '__all__'
        read_only_fields = ('slug',)

    def validate_price_per_service(self, value):
        if value < 0:
            raise ValidationError("قیمت هر سرویس نمی‌تواند مقدار منفی داشته باشد.")
        return value

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
