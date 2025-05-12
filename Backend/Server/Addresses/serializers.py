from rest_framework import serializers
from .models import Province, City, RecipientAddress




# ProvinceSerializer is simple as Province has no parent.
class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name', 'slug']
        read_only_fields = ['slug']

    def create(self, validated_data):
        # The model's save() method will generate the slug if missing.
        instance = Province.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance



# City is a child of Province.
class CitySerializer(serializers.ModelSerializer):
    # Return nested province details for read.
    province = ProvinceSerializer(read_only=True)
    # For write operations, we require the client's input as province_slug.
    province_slug = serializers.CharField(
        write_only=True,
        help_text="Slug of the associated province."
    )
    
    class Meta:
        model = City
        fields = ['id', 'province', 'province_slug', 'name', 'slug']
        read_only_fields = ['slug']
    
    def validate(self, attrs):
        # Use the provided province_slug to get the Province instance.
        data = self.initial_data  # raw input data
        province_slug = data.get('province_slug')
        if not province_slug:
            raise serializers.ValidationError({
                "province_slug": "This field is required."
            })
        try:
            province = Province.objects.get(slug=province_slug)
        except Province.DoesNotExist:
            raise serializers.ValidationError({
                "province_slug": f"No Province exists with the slug '{province_slug}'."
            })
        attrs['province'] = province
        return attrs

    def create(self, validated_data):
        # Remove the write-only field since we already used it to look up province.
        validated_data.pop('province_slug', None)
        return City.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # If a new province_slug is provided, update the related province.
        if 'province_slug' in self.initial_data:
            province_slug = self.initial_data.get('province_slug')
            try:
                province = Province.objects.get(slug=province_slug)
            except Province.DoesNotExist:
                raise serializers.ValidationError({
                    "province_slug": f"No Province exists with the slug '{province_slug}'."
                })
            instance.province = province
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance



class RecipientAddressSerializer(serializers.ModelSerializer):
    # Return nested city details for read.
    city = CitySerializer(read_only=True)
    # For write operations, accept a city_slug instead of a PK.
    city_slug = serializers.CharField(
        write_only=True,
        help_text="Slug of the associated city."
    )
    # For read operations, display the recipient's username.
    Recipient = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    
    class Meta:
        model = RecipientAddress
        fields = [
            'id', 'city', 'city_slug', 'Recipient', 
            'title', 'address', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate(self, attrs):
        data = self.initial_data
        city_slug = data.get('city_slug')
        if not city_slug:
            raise serializers.ValidationError({
                "city_slug": "This field is required."
            })
        try:
            city = City.objects.get(slug=city_slug)
        except City.DoesNotExist:
            raise serializers.ValidationError({
                "city_slug": f"No City exists with the slug '{city_slug}'."
            })
        attrs['city'] = city
        return attrs
    
    def create(self, validated_data):
        # Remove the write-only field.
        validated_data.pop('city_slug', None)
        # Automatically assign the current user as the Recipient.
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            validated_data['Recipient'] = request.user
        else:
            raise serializers.ValidationError("Authenticated user required.")
        return RecipientAddress.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        if 'city_slug' in self.initial_data:
            city_slug = self.initial_data.get('city_slug')
            try:
                city = City.objects.get(slug=city_slug)
            except City.DoesNotExist:
                raise serializers.ValidationError({
                    "city_slug": f"No City exists with the slug '{city_slug}'."
                })
            instance.city = city
        instance.title = validated_data.get('title', instance.title)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance
