from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Invoice, InvoiceItem




class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0
    fields = ('service', 'amount', 'created_at')
    readonly_fields = ('amount', 'created_at')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'company',
        'total_amount',
        'is_paid',
        'deadline',
        'deadline_status',
        'display_overdue',
        'created_at'
    )
    list_filter = ('is_paid', 'deadline_status', 'company')
    search_fields = ('company__name',)
    readonly_fields = ('total_amount', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    inlines = [InvoiceItemInline]

    def display_overdue(self, obj):
        return obj.is_overdue
    display_overdue.boolean = True
    display_overdue.short_description = 'Overdue?'

@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'service', 'amount', 'created_at')
    search_fields = ('invoice__company__name', 'service__title',)
    list_filter = ('invoice',)
    readonly_fields = ('amount', 'created_at')
