from django.utils.crypto import get_random_string
from rest_framework import serializers
from rest_framework import validators

from rest_framework_simplejwt.tokens import RefreshToken

from Users.models import User, IdCardInFormation
from .models import OneTimePassword

from random import randint





class OneTimePasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = OneTimePassword
        fields = "__all__"  
    

    def create(self, validated_data):
        code = randint(100000, 999999)
        token = get_random_string(100)
        otp = OneTimePassword.objects.create(
            phone=validated_data['phone'],
            token=token,
            code=code
        )
        otp.save()
        otp.get_expiration()
        return {'token': token, 'code': code}