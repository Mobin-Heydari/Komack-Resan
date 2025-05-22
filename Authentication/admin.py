from django.contrib import admin
from django.contrib.auth.models import Group

from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

from .models import UserRegisterOTP, UserLoginOTP




@admin.register(UserRegisterOTP)
class UserRegisterOTPAdmin(admin.ModelAdmin):
    list_display = (
        'username', 
        'email', 
        'phone', 
        'user_type', 
        'get_otp_token', 
        'created_at'
    )
    search_fields = ('username', 'email', 'phone')
    list_filter = ('user_type', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ("اطلاعات کاربر", {
            'fields': ('username', 'full_name', 'email', 'phone', 'user_type')
        }),
        ("اطلاعات رمز", {
            'fields': ('password', 'password_conf')
        }),
        ("OTP مرتبط", {
            'fields': ('otp',)
        }),
        ("زمان ثبت", {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_otp_token(self, obj):
        # Display the OTP token (as a string) from the related OneTimePassword record.
        return str(obj.otp.token)
    get_otp_token.short_description = "توکن OTP"


@admin.register(UserLoginOTP)
class UserLoginOTPAdmin(admin.ModelAdmin):
    list_display = (
        'get_user_phone', 
        'get_otp_token', 
        'phone', 
        'created_at'
    )
    search_fields = ('user__username', 'user__phone', 'otp__token', 'phone')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ("اطلاعات ورود", {
            'fields': ('user', 'otp', 'phone')
        }),
        ("زمان ثبت", {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_user_phone(self, obj):
        return obj.user.phone
    get_user_phone.short_description = "شماره کاربر"
    
    def get_otp_token(self, obj):
        return str(obj.otp.token)
    get_otp_token.short_description = "توکن OTP"

admin.site.unregister(Group)

admin.site.unregister(OutstandingToken)

admin.site.unregister(BlacklistedToken)