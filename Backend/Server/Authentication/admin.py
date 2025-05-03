from django.contrib import admin
from .models import OneTimePassword, UserRegisterOTP


admin.site.register(OneTimePassword)
admin.site.register(UserRegisterOTP)