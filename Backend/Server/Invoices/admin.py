from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from .models import Invoice, InvoiceItem



class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0
    readonly_fields = ('created_at',)  # Only creation time remains read-only.
    fields = ('service', 'amount', 'created_at')



@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'company',
        'formatted_deadline',
        'total_amount',
        'is_paid',
        'deadline_status',
        'is_overdue_display',
        'created_at',
    )
    list_filter = ('is_paid', 'deadline_status', 'company__industry', 'created_at')
    search_fields = ('company__name', 'id')
    date_hierarchy = 'created_at'
    readonly_fields = (
        'created_at',
        'updated_at',
        'calculate_total_message',
        'is_overdue_display',
    )
    
    fieldsets = (
        ("مشخصات قبض", {
            'fields': (
                'company',
                'total_amount',
                'is_paid',
                'deadline',
                'deadline_status',
                'calculate_total_message',
            )
        }),
        ("تاریخ‌ها", {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    inlines = [InvoiceItemInline]
    
    @admin.display(description="مهلت پرداخت (فرمت)")
    def formatted_deadline(self, obj):
        if obj.deadline:
            return obj.deadline.strftime("%Y-%m-%d %H:%M")
        return "-"
    
    @admin.display(description="فاکتور منقضی شده؟")
    def is_overdue_display(self, obj):
        return "بله" if obj.is_overdue else "خیر"
    
    @admin.display(description="به‌روزرسانی مبلغ کل")
    def calculate_total_message(self, obj):
        """
        This read-only field reminds the admin that once changes are saved,
        the invoice's total_amount will be calculated automatically via
        the Invoice.calculate_total() method.
        """
        return format_html('<span style="color: #555;">برای به‌روزرسانی مبلغ کل، صفحه را ذخیره کنید.</span>')


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'service', 'amount', 'created_at')
    search_fields = ('invoice__company__name', 'service__title')
    list_filter = ('invoice__company', 'created_at')
    readonly_fields = ('created_at',)
