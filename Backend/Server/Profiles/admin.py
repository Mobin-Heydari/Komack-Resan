from django.contrib import admin
from django.utils.html import format_html
from .models import (
    ServiceProviderProfile,
    ServiceRecipientProfile,
    AdminProfile,
    SupportProfile,
)

# Base admin class for common profile functionality.
class BaseProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'age', 'created_at', 'updated_at', 'profile_picture_preview')
    search_fields = ('user__username', 'user__full_name')
    list_filter = ('gender',)
    readonly_fields = ('created_at', 'updated_at')

    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />',
                obj.profile_picture.url
            )
        return "-"
    profile_picture_preview.short_description = "تصویر پروفایل"


@admin.register(ServiceProviderProfile)
class ServiceProviderProfileAdmin(BaseProfileAdmin):
    list_display = BaseProfileAdmin.list_display + ('is_available',)
    list_filter = BaseProfileAdmin.list_filter + ('is_available',)
    # Optionally, you may add extra fields or customizations here.


@admin.register(ServiceRecipientProfile)
class ServiceRecipientProfileAdmin(BaseProfileAdmin):
    pass


@admin.register(AdminProfile)
class AdminProfileAdmin(BaseProfileAdmin):
    pass


@admin.register(SupportProfile)
class SupportProfileAdmin(BaseProfileAdmin):
    pass
