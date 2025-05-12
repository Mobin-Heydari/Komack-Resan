from django.shortcuts import get_object_or_404

from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import ValidationError

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer, UserRegisterOneTimePasswordSerializer, UserRegisterSerializer, UserLoginOneTimePasswordSerializer, UserLoginValidateOneTimePasswordSerializer
from .models import OneTimePassword, UserRegisterOTP, UserLoginOTP

from Users.models import User




class LoginAPIView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if request.user.is_authenticated:
            return Response({"message": "شما قبلاً وارد شده‌اید"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if serializer.is_valid():
                phone = serializer.validated_data['phone']
                user = User.objects.get(phone=phone)

                if not user.is_active:
                    return Response({'error': 'کاربر فعال نیست'}, status=status.HTTP_401_UNAUTHORIZED)
                
                refresh = RefreshToken.for_user(user)
                
                return Response(
                    {
                        'refresh': str(refresh), 
                        'access': str(refresh.access_token)
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            return Response({'error': 'خطای اعتبارسنجی'}, status=status.HTTP_400_BAD_REQUEST)
        return super().handle_exception(exc)



class UserRegisterOtpAPIView(APIView):

    def post(self, request):
        
        if not request.user.is_authenticated:  

            serializer = UserRegisterOneTimePasswordSerializer(data=request.data)

            if serializer.is_valid(raise_exception=True):

                otp_data = serializer.create(validated_data=serializer.validated_data)

                return Response(
                    {
                        'Detail': {
                            'Message': 'Otp created successfully',
                            'token': otp_data['token'], 
                            'code': otp_data['code']
                        }
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Detail': 'You are already logged in'}, status=status.HTTP_400_BAD_REQUEST)



class UserRegisterOtpValidateAPIView(APIView):

    def post(self, request, token):

        if not request.user.is_authenticated:
            otp = get_object_or_404(OneTimePassword, token=token)
            if otp:
                if otp.registration_otps:
                    serializer = UserRegisterSerializer(data=request.data, context={'otp_token': otp.token})
                    if serializer.is_valid(raise_exception=True):

                        user_data = serializer.create(
                            validated_data=serializer.validated_data, 
                            token=token
                        )

                        return Response(
                            {
                                'Detail': {
                                    'Message': 'User created successfully',
                                    'User': user_data['user'],
                                    'Token': user_data['tokens']
                                }
                            },
                            status=status.HTTP_201_CREATED
                        )
                    else:
                        return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'Detail': 'Otp register does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'Detail': 'OTP does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'Detail': 'You are already authenticated'}, status=status.HTTP_400_BAD_REQUEST)



class UserLoginOneTimePasswordAPIView(APIView):

    def post(self, request):
        if not request.user.is_authenticated:
            serializer = UserLoginOneTimePasswordSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                otp_data = serializer.create(validated_data=serializer.validated_data)

                return Response(
                    {
                        'Detail': {
                            'Message': 'Otp created successfully',
                            'token': otp_data['token'], 
                            'code': otp_data['code']
                        }
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Detail': 'You are already logged in'}, status=status.HTTP_400_BAD_REQUEST)



class UserLoginValidateOneTimePasswordAPIView(APIView):
    def post(self, request, token):
        otp = get_object_or_404(OneTimePassword, token=token)

        login_otp = otp.login_otps.get()
        
        serializer = UserLoginValidateOneTimePasswordSerializer(data=request.data, context={'otp_token': token})

        if request.user.is_authenticated:
            return Response({"message": "شما قبلاً وارد شده‌اید"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if serializer.is_valid():
                user = login_otp.user

                if not user.is_active:
                    return Response({'error': 'کاربر فعال نیست'}, status=status.HTTP_401_UNAUTHORIZED)
                
                refresh = RefreshToken.for_user(user)
                
                return Response(
                    {
                        'refresh': str(refresh), 
                        'access': str(refresh.access_token)
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            return Response({'error': 'خطای اعتبارسنجی'}, status=status.HTTP_400_BAD_REQUEST)
        return super().handle_exception(exc)