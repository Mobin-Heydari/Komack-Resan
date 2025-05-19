from django.contrib import admin
from .models import UserRegisterOTP



@admin.register(UserRegisterOTP)
class UserRegisterOTPAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'phone',
        'user_type',
        'otp_token',
        'created_at'
    )
    search_fields = ('username', 'email', 'phone', 'user_type')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'otp')
    fieldsets = (
        (None, {
            'fields': (
                'username',
                'email',
                'phone',
                'password',
                'password_conf',
                'full_name',
                'user_type',
                'otp'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def otp_token(self, obj):
        return str(obj.otp.token)
    otp_token.short_description = "OTP Token"
