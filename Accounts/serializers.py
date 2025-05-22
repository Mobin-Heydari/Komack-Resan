from rest_framework import serializers

from .models import ResetPasswordOneTimePassword

from Users.models import User
from Authentication.models import OneTimePassword
from OneTimePasswords.serializers import OneTimePasswordSerializer

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
    password = serializers.CharField(max_length=16, min_length=8, required=True)
    password_conf = serializers.CharField(max_length=16, min_length=8, required=True)

     # Validate the password field
    def validate_password(self, value):
        # Check if the password length is within the allowed range
        if len(value) < 8 or len(value) > 16:
            raise serializers.ValidationError('Password must be at least 8 characters long and the most 16 characters long')
        return value

    # Validate the password_conf field
    def validate_password_conf(self, value):
        # Check if the password_conf length is within the allowed range
        if len(value) < 8 or len(value) > 16:
            raise serializers.ValidationError('Password must be at least 8 characters long and the most 16 characters long')
        return value
    
    
    def validate(self, attrs):
        otp_token = self.context.get('otp_token')
        
        otp = OneTimePassword.objects.get(token=otp_token)
        try:
            reset_password_otp = otp.reset_password.get()
        except:
            raise serializers.ValidationError('The otp is not a reset password otp.')

        if otp.status_validation() == 'ACT':
            if otp.code == attrs['code']:
                # Check if the password and password_conf match
                if attrs['password'] != attrs['password_conf']:
                    raise serializers.ValidationError('Passwords do not match')
                if len(attrs['password']) < 8 or len(attrs['password']) > 16:
                    raise serializers.ValidationError('Password must be between 8 and 16 characters long')
                return attrs
            else:
                raise serializers.ValidationError({'code': 'Invalid OTP code.'})
        else:
            otp.delete()
            reset_password_otp.delete()
            raise serializers.ValidationError('Inactive OTP')