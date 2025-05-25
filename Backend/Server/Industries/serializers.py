from django.utils.text import slugify

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
    
    def create(self, validated_data):
        category = IndustryCategory.objects.create(
            slug=validated_data['slug'],
            name=validated_data['name'],
            icon=validated_data['icon']
        )
        
        category.save()

        return category


class IndustrySerializer(serializers.ModelSerializer):
    category = IndustryCategorySerializer(read_only=True)
    category_slug = serializers.CharField(write_only=True, required=False)
    name = serializers.CharField(required=False)

    class Meta:
        model = Industry
        fields = '__all__'
        read_only_fields = ('slug', 'category',)

    def validate_price_per_service(self, value):
        if value < 0:
            raise ValidationError("قیمت هر سرویس نمی‌تواند مقدار منفی داشته باشد.")
        return value


    def update(self, instance, validated_data):
        category_slug = validated_data.pop('category_slug', None)
        if category_slug:
            category = IndustryCategory.objects.get(slug=category_slug)
            validated_data['category'] = category
        return super().update(instance, validated_data)

    

    def create(self, validated_data):

        category_slug = validated_data.pop('category_slug', None)

        if not category_slug:
            raise ValidationError('category is required')
        
        category = IndustryCategory.objects.get(slug=category_slug)

        industry = Industry.objects.create(
            slug=validated_data['slug'],
            category=category,
            name=validated_data['name'],
            icon=validated_data['icon'],
            price_per_service=validated_data['price_per_service'],
        )
        
        industry.save()

        return industry