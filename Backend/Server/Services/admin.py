from django.contrib import admin
from .models import Service, ServiceEmployee




# Inline for ServiceEmployees
class ServiceEmployeeInline(admin.TabularInline):
    model = ServiceEmployee
    extra = 0
    fields = ('job_title', 'employee', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'company', 
        'service_provider', 
        'recipient', 
        'payment_status', 
        'service_status', 
        'started_at', 
        'finished_at'
    )
    search_fields = (
        'title', 
        'company__name', 
        'service_provider__username', 
        'recipient__username'
    )
    list_filter = ('payment_status', 'service_status', 'is_invoiced')
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ServiceEmployeeInline]
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ServiceEmployee)
class ServiceEmployeeAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'recipient_service', 'employee', 'created_at')
    search_fields = (
        'job_title', 
        'recipient_service__title', 
        'employee__employee__username'
    )
    list_filter = ('job_title',)
    readonly_fields = ('created_at', 'updated_at')
