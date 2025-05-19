from django.contrib import admin
from .models import ResetPasswordOneTimePassword



@admin.register(ResetPasswordOneTimePassword)
class ResetPasswordOneTimePasswordAdmin(admin.ModelAdmin):
    list_display = (
        'get_otp_token', 
        'get_otp_code', 
        'user', 
        'phone', 
        'created_at'
    )
    search_fields = (
        'user__username', 
        'otp__token', 
        'otp__code', 
        'phone'
    )
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ("اطلاعات کد اعتبار سنجی", {
            'fields': ('otp',)
        }),
        ("اطلاعات کاربر", {
            'fields': ('user', 'phone')
        }),
        ("زمان ثبت", {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    @admin.display(description="توکن OTP")
    def get_otp_token(self, obj):
        return str(obj.otp.token)
    
    @admin.display(description="کد OTP")
    def get_otp_code(self, obj):
        return obj.otp.code
