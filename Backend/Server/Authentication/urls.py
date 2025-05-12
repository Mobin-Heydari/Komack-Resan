from django.urls import path
from . import views



app_name = "Authentication"



urlpatterns = [
    path('login/', views.LoginAPIView.as_view(), name="login"),

    path('login-otp/', views.UserLoginOneTimePasswordAPIView.as_view()),
    
    path('login-validate-otp/<str:token>/', views.UserLoginValidateOneTimePasswordAPIView.as_view()),

    path('register-otp/', views.UserRegisterOtpAPIView.as_view(), name="user_register_otp"),

    path('validate-otp/<str:token>/', views.UserRegisterOtpValidateAPIView.as_view(), name="user_register_otp_validate"),
]