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
    


class LoginSerializer(serializers.Serializer):

    phone = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
    

    def validate_phone(self, value):
        if not User.objects.filter(phone=value).exists():
            raise serializers.ValidationError('شماره تلفن موجود نیست')
        return value


    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('رمز عبور باید حداقل ۸ کاراکتر باشد')
        return value


    def validate(self, data):
        phone = data.get('phone')
        password = data.get('password')
        if phone is None or password is None:
            raise serializers.ValidationError('شماره تلفن و رمز عبور هر دو الزامی هستند')
        user = User.objects.get(phone=phone)
        if not user.check_password(password):
            raise serializers.ValidationError('رمز عبور اشتباه است')
        return data