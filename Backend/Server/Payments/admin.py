from django.contrib import admin
from .models import PaymentInvoice

@admin.register(PaymentInvoice)
class PaymentInvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'invoice',
        'amount',
        'payment_status',
        'transaction_id',
        'created_at',
        'updated_at',
    )
    list_filter = ('payment_status', 'created_at')
    search_fields = (
        'invoice__id',
        'transaction_id',
    )
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at',)

    fieldsets = (
        (None, {
            'fields': ('invoice', 'amount', 'payment_status', 'transaction_id')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
