from rest_framework import serializers

from .models import ResetPasswordOneTimePassword

from Users.models import User
from Authentication.models import OneTimePassword
from Authentication.serializers import OneTimePasswordSerializer

from random import randint
import uuid





class ResetPasswordOneTimePasswordSerializer(serializers.Serializer):

    phone = serializers.CharField(required=True, write_only=True)

    def validate_phone(self, value):
        if value is None:
            raise serializers.ValidationError('شماره تلفن الزامی است')
        return value

    def validate(self, atters):
        if User.objects.filter(phone=atters['phone']).exists():
            return atters
        else:
            raise serializers.ValidationError('شماره تلفن موجود نیست')

    def create(self, validated_data):

        code = randint(100000, 999999)

        token = uuid.uuid4()
        
        otp = OneTimePassword.objects.create(
            token=token,
            code=code
        )
        
        otp.save()

        otp.get_expiration()
        
        user = User.objects.get(phone=validated_data['phone'])
        
        reset_password_otp = ResetPasswordOneTimePassword.objects.create(
            otp=otp,
            user=user,
            phone=validated_data['phone']
        )

        reset_password_otp.save()

        return {'phone': reset_password_otp.phone, 'token': token, 'code': code}



class ResetPasswordValidateOneTimePasswordSerializer(serializers.Serializer):

    code = serializers.CharField(max_length=6, min_length=6, required=True)

    def validate(self, attrs):
        otp_token = self.context.get('otp_token')
        
        otp = OneTimePassword.objects.get(token=otp_token)

        if otp.status_validation() == 'ACT':
            if otp.code == attrs['code']:
                return attrs
            else:
                raise serializers.ValidationError({'code': 'Invalid OTP code.'})
        else:
            raise serializers.ValidationError('Inactive OTP')