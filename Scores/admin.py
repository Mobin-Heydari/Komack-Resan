from django.contrib import admin
from .models import ServiceScore

@admin.register(ServiceScore)
class ServiceScoreAdmin(admin.ModelAdmin):
    list_display = (
        'service', 
        'quality', 
        'behavior', 
        'time', 
        'created_at'
    )
    search_fields = ('service__title',)
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)

    fieldsets = (
        ("اطلاعات سرویس", {
            'fields': ('service',)
        }),
        ("امتیازات", {
            'fields': ('quality', 'behavior', 'time',)
        }),
        ("زمان ثبت", {
            'fields': ('created_at',)
        }),
    )