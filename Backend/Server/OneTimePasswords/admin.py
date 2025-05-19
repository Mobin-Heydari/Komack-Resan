from django.contrib import admin
from django.utils import timezone
from .models import OneTimePassword



@admin.register(OneTimePassword)
class OneTimePasswordAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'token',
        'status',
        'is_used',
        'formatted_expiration',
        'created_at',
        'updated_at',
    )
    search_fields = ('code', 'token')
    list_filter = ('status', 'is_used', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['recalculate_expiration_action', 'validate_status_action']
    
    @admin.display(description="مهلت (تاریخ انقضا)")
    def formatted_expiration(self, obj):
        if obj.expiration:
            return obj.expiration.strftime("%Y-%m-%d %H:%M")
        return "تنظیم نشده"
    
    def recalculate_expiration_action(self, request, queryset):
        updated_count = 0
        for otp in queryset:
            otp.get_expiration()  # Updates and saves the expiration
            updated_count += 1
        self.message_user(request, f"{updated_count} رمز یکبار مصرف بروز شد.")
    recalculate_expiration_action.short_description = "بروز کردن تاریخ انقضا برای رمزهای یکبارمصرف انتخاب‌شده"
    
    def validate_status_action(self, request, queryset):
        updated_count = 0
        for otp in queryset:
            otp.status_validation()  # Updates the status according to usage and expiration
            otp.save(update_fields=["status"])
            updated_count += 1
        self.message_user(request, f"{updated_count} وضعیت رمزهای یکبارمصرف به‌روزرسانی شد.")
    validate_status_action.short_description = "اعتبارسنجی وضعیت OTP های انتخاب‌شده"
