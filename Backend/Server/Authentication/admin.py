from django.contrib import admin
from .models import OneTimePassword, UserRegisterOTP

@admin.register(OneTimePassword)
class OneTimePasswordAdmin(admin.ModelAdmin):
    list_display = (
        'token',
        'code',
        'status',
        'is_used',
        'expiration',
        'created_at'
    )
    search_fields = ('token', 'code')
    list_filter = ('status', 'is_used')
    ordering = ('-created_at',)
    readonly_fields = ('token', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('token', 'code', 'status', 'is_used', 'expiration')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

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
