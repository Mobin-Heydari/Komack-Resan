from django.contrib import admin
from django.utils.html import format_html
from .models import Service, ServiceContent, ServiceEmployees


# Inline for ServiceContent
class ServiceContentInline(admin.TabularInline):
    model = ServiceContent
    extra = 0
    fields = ('title', 'image_preview', 'video', 'created_at')
    readonly_fields = ('image_preview', 'created_at')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" style="height:auto;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Preview Image"


# Inline for ServiceEmployees
class ServiceEmployeesInline(admin.TabularInline):
    model = ServiceEmployees
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
    inlines = [ServiceContentInline, ServiceEmployeesInline]
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ServiceContent)
class ServiceContentAdmin(admin.ModelAdmin):
    list_display = ('service', 'title', 'image_preview', 'created_at')
    search_fields = ('service__title', 'title')
    list_filter = ('service',)
    readonly_fields = ('created_at', 'updated_at')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" style="height:auto;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Preview Image"


@admin.register(ServiceEmployees)
class ServiceEmployeesAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'recipient_service', 'employee', 'created_at')
    search_fields = (
        'job_title', 
        'recipient_service__title', 
        'employee__employee__username'
    )
    list_filter = ('job_title',)
    readonly_fields = ('created_at', 'updated_at')
