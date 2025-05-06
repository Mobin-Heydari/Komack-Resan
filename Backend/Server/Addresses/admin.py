from django.contrib import admin
from .models import RecipientAddress



@admin.register(RecipientAddress)
class RecipientAddressAdmin(admin.ModelAdmin):
    list_display = ('Recipient', 'title', 'address', 'created_at', 'updated_at')
    search_fields = ('title', 'address', 'Recipient__username', 'Recipient__full_name')
    list_filter = ('Recipient',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('Recipient', 'title', 'address')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
