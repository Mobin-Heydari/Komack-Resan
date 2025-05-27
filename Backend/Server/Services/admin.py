from django.contrib import admin
from django.utils.html import format_html
from .models import Service




@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'company',
        'recipient',
        'payment_status',
        'service_status',
        'payment_method',
        'is_invoiced',
        'overall_score_display',
        'created_at'
    )
    list_filter = ('payment_status', 'service_status', 'payment_method', 'is_invoiced', 'company')
    search_fields = (
        'title', 
        'descriptions', 
        'company__name', 
        'service_provider__username', 
        'recipient__username'
    )
    readonly_fields = (
        'created_at', 
        'updated_at', 
        'overall_score_display', 
        'transaction_screenshot_preview'
    )
    
    fieldsets = (
        ("اطلاعات اولیه سرویس", {
            'fields': (
                'company', 
                'company_card', 
                'recipient', 
                'recipient_address', 
                'title', 
                'slug', 
                'descriptions'
            )
        }),
        ("وضعیت سرویس و پرداخت", {
            'fields': (
                'payment_status', 
                'service_status', 
                'payment_method', 
                'is_invoiced', 
                'transaction_screenshot', 
                'transaction_screenshot_preview'
            )
        }),
        ("زمانبندی", {
            'fields': ('started_at', 'finished_at')
        }),
        ("تاریخ‌ها", {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def overall_score_display(self, obj):
        if obj.overall_score is not None:
            return f"{obj.overall_score:.2f}"
        return "ندارد"
    overall_score_display.short_description = "امتیاز کلی"
    
    def transaction_screenshot_preview(self, obj):
        if obj.transaction_screenshot:
            return format_html('<img src="{}" width="100" height="100" />', obj.transaction_screenshot.url)
        return "فاقد تصویر"
    transaction_screenshot_preview.short_description = "پیش نمایش فاکتور تراکنش"