from django.urls import path
from . import views



app_name = "Accounts"



urlpatterns = [
    path('reset-password-otp/', views.ResetPasswordOneTimePasswordAPIView.as_view(), name="reset_password_otp"),

    path('reset-password-validate-otp/<str:token>/', views.ResetPasswordValidateOneTimePasswordAPIView.as_view(), name="reset_password_otp_validate"),
]