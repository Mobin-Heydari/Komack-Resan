from django.contrib import admin
from django.utils.html import format_html
from .models import PaymentInvoice


@admin.register(PaymentInvoice)
class PaymentInvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'invoice',
        'amount',
        'transaction_id',
        'payment_status_display',
        'timestamp',
        'created_at'
    )
    list_filter = ('payment_status', 'created_at')
    search_fields = ('invoice__id', 'transaction_id', 'invoice__company__name')
    readonly_fields = ('timestamp', 'created_at', 'updated_at')
    actions = ['mark_successful_action']
    
    fieldsets = (
        ("اطلاعات پرداخت", {
            'fields': ('invoice', 'amount', 'transaction_id', 'authority', 'payment_status'),
        }),
        ("زمان‌بندی", {
            'fields': ('timestamp', 'created_at', 'updated_at'),
        }),
    )
    
    @admin.display(description="وضعیت پرداخت")
    def payment_status_display(self, obj):
        return obj.get_payment_status_display()
    
    def mark_successful_action(self, request, queryset):
        count = 0
        for payment in queryset:
            if payment.payment_status != payment.PaymentStatusChoices.SUCCESS:
                payment.mark_successful()
                count += 1
        self.message_user(request, f"{count} پرداخت به عنوان موفق علامت گذاری شد.")
    mark_successful_action.short_description = "علامت گذاری پرداخت‌های انتخاب شده به عنوان موفق"
