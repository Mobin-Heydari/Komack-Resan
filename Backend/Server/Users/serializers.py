from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'full_name',
            'email',
            'phone',
            'user_type',
            'status',
            'joined_date',
            'last_updated',
        ]
        read_only_fields = ['id', 'joined_date', 'last_updated']