from rest_framework import serializers
from rest_framework import validators
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserRegisterOTP, UserLoginOTP

from Users.models import User, IdCardInFormation
from OneTimePasswords.models import OneTimePassword

from random import randint
import uuid




    


class PasswordLoginSerializer(serializers.Serializer):

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
    


class UserRegisterOneTimePasswordSerializer(serializers.ModelSerializer):

    # Define the email field with validation to ensure uniqueness
    email = serializers.EmailField(
        validators=[
            validators.UniqueValidator(queryset=User.objects.all())  # Ensure email is unique in User model
        ],
        required=True,  # Email is required
        help_text="Enter a unique email address"  # Help text for the email field
    )

    # Define the username field
    username = serializers.CharField(
        validators=[
            validators.UniqueValidator(queryset=User.objects.all())  # Ensure username is unique in User model
        ],
        required=True,  # Username is required
        help_text="Enter a unique username"  # Help text for the username field
    )

    # Define the full name field
    full_name = serializers.CharField(
        required=True,  # Full name is required
        help_text="Enter your full name"  # Help text for the full name field
    )

    # Define the password field with validation
    password = serializers.CharField(
        required=True,  # Password is required
        write_only=True,  # Password is not returned in the response
        help_text="Enter a password (8-16 characters)"  # Help text for the password field
    )

    # Define the password confirmation field
    password_conf = serializers.CharField(
        required=True,  # Password confirmation is required
        write_only=True,  # Password confirmation is not returned in the response
        help_text="Confirm your password (8-16 characters)"  # Help text for the password confirmation field
    )

    user_type = serializers.CharField(required=True, write_only=True)


    class Meta:
        model = UserRegisterOTP
        fields = "__all__"
        read_only_fields = ['otp']

    
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

    # Validate the username field
    def validate_username(self, value):
        # Check if the username length is within the allowed range
        if len(value) < 3 or len(value) > 20:
            raise serializers.ValidationError('Username must be between 3 and 20 characters long')
        return value

    # Validate the full name field
    def validate_full_name(self, value):
        # Check if the full name length is within the allowed range
        if len(value) < 3 or len(value) > 50:
            raise serializers.ValidationError('Full name must be between 3 and 50 characters long')
        return value
    
    def validate_user_type(self, value):
        if len(value) != 2:
            raise serializers.ValidationError("The user type must have a length of 2.")
        if value not in ('OW', 'SC', 'SP'):
            raise serializers.ValidationError("The user type must be one of the following: OW, SC, SP.")
        return value



    # Validate the entire serializer
    def validate(self, attrs):
        # Check if the password and password_conf match
        if attrs['password'] != attrs['password_conf']:
            raise serializers.ValidationError('Passwords do not match')
        if attrs['password'] == attrs['username']:
            raise serializers.ValidationError('Password cannot be the same as the username')
        if len(attrs['password']) < 8 or len(attrs['password']) > 16:
            raise serializers.ValidationError('Password must be between 8 and 16 characters long')
        return attrs



    def create(self, validated_data):

        code = randint(100000, 999999)

        token = uuid.uuid4()

        otp = OneTimePassword.objects.create(
            token=token,
            code=code
        )

        otp.save()

        otp.get_expiration()

        user_register_otp = UserRegisterOTP.objects.create(
            otp=otp,
            email=validated_data['email'],
            phone=validated_data['phone'],
            username=validated_data['username'],
            password=validated_data['password'],
            user_type=validated_data['user_type'],
            full_name=validated_data['full_name'],
            password_conf=validated_data['password_conf']
        )


        user_register_otp.save()

        return {'phone': user_register_otp.phone, 'token': token, 'code': code}
    


class UserRegisterValidateOneTimePasswordSerializer(serializers.Serializer):

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
    

    def create(self, validated_data, token):

        otp = OneTimePassword.objects.get(token=token)

        otp.is_used = True
        otp.save()

        user_register_otp = otp.registration_otps

        id_card_info = IdCardInFormation.objects.create()

        user = User.objects.create_user(
            email=user_register_otp.email,
            phone=user_register_otp.phone,
            username=user_register_otp.username,
            password=user_register_otp.password,
            full_name=user_register_otp.full_name,
            user_type=user_register_otp.user_type
        )

        user.id_card_info = id_card_info

        user.save()

        refresh = RefreshToken.for_user(user)

        return {
            'user': {
                'username': user.username,
                'email': user.email,
                'phone': user.phone,
                'user_type': user.user_type
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }
    


class UserLoginOneTimePasswordSerializer(serializers.Serializer):

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
        
        user_login_otp = UserLoginOTP.objects.create(
            otp=otp,
            user=user,
            phone=validated_data['phone']
        )

        user_login_otp.save()

        return {'phone': user_login_otp.phone, 'token': token, 'code': code}



class UserLoginValidateOneTimePasswordSerializer(serializers.Serializer):

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