from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import ServiceScore
from Services.models import Service



class ServiceScoreSerializer(serializers.ModelSerializer):
    # Computed field: returns the overall score rounded to 2 decimals.
    overall = serializers.SerializerMethodField(read_only=True)
    
    # Read-only field: shows the Service’s title.
    service = serializers.SlugRelatedField(read_only=True, slug_field='title')
    # Write-only field: accepts a service slug to look up the related Service.
    service_slug = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = ServiceScore
        fields = [
            'service',           # Display the service title.
            'service_slug',      # Input for looking up the service.
            'quality',
            'behavior',
            'time',
            'overall',           # Computed overall score.
            'created_at',
        ]
        read_only_fields = ['service', 'overall', 'created_at']
        validators = [
            UniqueTogetherValidator(
                queryset=ServiceScore.objects.all(),
                fields=['service'],
                message="A score for this service already exists."
            )
        ]
    
    def get_overall(self, obj):
        overall = obj.overall  # Uses the model’s property: (quality + behavior + time) / 3
        return round(overall, 2) if overall is not None else None
    
    def validate(self, attrs):
        """
        On creation:
          - Pop the 'service_slug' field and lookup the Service.
          - Raise an error if the Service does not exist.
          - Also, ensure that the Service does not already have a score.
        On update:
          - Disallow any change to the Service via service_slug.
        """
        if not self.instance:  # Create operation
            service_slug = attrs.pop('service_slug', None)
            if not service_slug:
                raise serializers.ValidationError({'service_slug': 'This field is required.'})
            try:
                service = Service.objects.get(slug=service_slug)
            except Service.DoesNotExist:
                raise serializers.ValidationError({'service_slug': 'Service with this slug does not exist.'})
            
            attrs['service'] = service
        else:
            # Update operation: Do not allow changing the associated service.
            if 'service_slug' in attrs:
                raise serializers.ValidationError({'service_slug': 'You cannot change the service on update.'})
        return attrs
    
    def create(self, validated_data):
        """
        Create and return a new ServiceScore instance.
        """
        return ServiceScore.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update only the mutable fields: quality, behavior, and time.
        """
        instance.quality = validated_data.get('quality', instance.quality)
        instance.behavior = validated_data.get('behavior', instance.behavior)
        instance.time = validated_data.get('time', instance.time)
        instance.save()
        return instance
