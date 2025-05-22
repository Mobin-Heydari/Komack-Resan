from django.shortcuts import get_object_or_404

from rest_framework.views import APIView, Response
from rest_framework.validators import ValidationError
from rest_framework import status

from .serializers import ResetPasswordOneTimePasswordSerializer, ResetPasswordValidateOneTimePasswordSerializer

from OneTimePasswords.models import OneTimePassword




class ResetPasswordOneTimePasswordAPIView(APIView):

    def post(self, request):
        if not request.user.is_authenticated:
            serializer = ResetPasswordOneTimePasswordSerializer(data=request.data)
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



class ResetPasswordValidateOneTimePasswordAPIView(APIView):
    def post(self, request, token):
        otp = get_object_or_404(OneTimePassword, token=token)

        reset_password_otp = otp.reset_password.get()
        
        serializer = ResetPasswordValidateOneTimePasswordSerializer(data=request.data, context={'otp_token': token})

        if request.user.is_authenticated:
            return Response({"message": "شما قبلاً وارد شده‌اید"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if serializer.is_valid():
                user = reset_password_otp.user

                if not user.is_active:
                    return Response({'error': 'کاربر فعال نیست'}, status=status.HTTP_401_UNAUTHORIZED)
                
                password = user.set_password(serializer.validated_data['password'])

                user.save()

                otp.delete()
                reset_password_otp.delete()
                
                return Response(
                    {
                        'Massage': 'Password reseted.',
                        'Password': serializer.validated_data['password']
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            return Response({'error': 'خطای اعتبارسنجی'}, status=status.HTTP_400_BAD_REQUEST)
        return super().handle_exception(exc)