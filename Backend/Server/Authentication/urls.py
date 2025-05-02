from django.urls import path
from . import views



app_name = "Authentication"



urlpatterns = [
    path('login/', views.LoginAPIView.as_view(), name="login"),
    path('register-otp/', views.UserRegisterOtpAPIView.as_view(), name="user_register_otp"),
]