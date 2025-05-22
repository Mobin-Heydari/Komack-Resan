from django.contrib import admin
from django.utils.html import format_html
from .models import (
    ServiceProviderProfile,
    ServiceRecipientProfile,
    AdminProfile,
    SupportProfile
)

class ProfileAdminBase(admin.ModelAdmin):
    # Declare read-only fields (including our custom method)
    readonly_fields = ('created_at', 'updated_at', 'profile_picture_preview',)

    def profile_picture_preview(self, obj):
        """
        Returns an HTML img tag with a fixed size to preview the profile picture.
        """
        if obj.profile_picture:
            return format_html(
                '<img src="{}" style="max-width:50px; max-height:50px;" />',
                obj.profile_picture.url
            )
        return "فاقد تصویر"
    profile_picture_preview.short_description = "نمایش تصویر"

    def get_fieldsets(self, request, obj=None):
        """
        Use add_fieldsets when creating a new object (obj is None). Otherwise,
        use the normal fieldsets.
        """
        if obj is None and hasattr(self, 'add_fieldsets'):
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)


#-------------------------------------------------
# Service Provider Profile Admin
#-------------------------------------------------
@admin.register(ServiceProviderProfile)
class ServiceProviderProfileAdmin(ProfileAdminBase):
    list_display = (
        'user',
        'gender',
        'age',
        'experience_years',
        'is_available',
        'profile_picture_preview',
        'created_at'
    )
    list_filter = ('gender', 'is_available',)
    search_fields = ('user__username', 'bio',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ("اطلاعات کاربری", {
            'fields': ('user',)
        }),
        ("مشخصات فردی", {
            'fields': ('gender', 'age', 'bio', 'profile_picture', 'profile_picture_preview')
        }),
        ("جزئیات تجربه", {
            'fields': ('experience_years', 'is_available')
        }),
        ("تاریخ‌ها", {
            'fields': ('created_at', 'updated_at')
        }),
    )
    add_fieldsets = (
        ("اطلاعات کاربری", {
            'fields': ('user',)
        }),
        ("مشخصات فردی", {
            'fields': ('gender', 'age', 'bio', 'profile_picture')
        }),
        ("جزئیات تجربه", {
            'fields': ('experience_years', 'is_available')
        }),
    )


#-------------------------------------------------
# Service Recipient Profile Admin
#-------------------------------------------------
@admin.register(ServiceRecipientProfile)
class ServiceRecipientProfileAdmin(ProfileAdminBase):
    list_display = (
        'user',
        'gender',
        'age',
        'profile_picture_preview',
        'created_at'
    )
    list_filter = ('gender',)
    search_fields = ('user__username', 'bio',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ("اطلاعات کاربری", {
            'fields': ('user',)
        }),
        ("مشخصات فردی", {
            'fields': ('gender', 'age', 'bio', 'profile_picture', 'profile_picture_preview')
        }),
        ("تاریخ‌ها", {
            'fields': ('created_at', 'updated_at')
        }),
    )
    add_fieldsets = (
        ("اطلاعات کاربری", {
            'fields': ('user',)
        }),
        ("مشخصات فردی", {
            'fields': ('gender', 'age', 'bio', 'profile_picture')
        }),
    )


#-------------------------------------------------
# Admin Profile Admin
#-------------------------------------------------
@admin.register(AdminProfile)
class AdminProfileAdmin(ProfileAdminBase):
    list_display = (
        'user',
        'gender',
        'age',
        'profile_picture_preview',
        'created_at'
    )
    list_filter = ('gender',)
    search_fields = ('user__username', 'bio',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ("اطلاعات کاربری", {
            'fields': ('user',)
        }),
        ("مشخصات فردی", {
            'fields': ('gender', 'age', 'bio', 'profile_picture', 'profile_picture_preview')
        }),
        ("تاریخ‌ها", {
            'fields': ('created_at', 'updated_at')
        }),
    )
    add_fieldsets = (
        ("اطلاعات کاربری", {
            'fields': ('user',)
        }),
        ("مشخصات فردی", {
            'fields': ('gender', 'age', 'bio', 'profile_picture')
        }),
    )


#-------------------------------------------------
# Support Profile Admin
#-------------------------------------------------
@admin.register(SupportProfile)
class SupportProfileAdmin(ProfileAdminBase):
    list_display = (
        'user',
        'gender',
        'age',
        'profile_picture_preview',
        'created_at'
    )
    list_filter = ('gender',)
    search_fields = ('user__username', 'bio',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ("اطلاعات کاربری", {
            'fields': ('user',)
        }),
        ("مشخصات فردی", {
            'fields': ('gender', 'age', 'bio', 'profile_picture', 'profile_picture_preview')
        }),
        ("تاریخ‌ها", {
            'fields': ('created_at', 'updated_at')
        }),
    )
    add_fieldsets = (
        ("اطلاعات کاربری", {
            'fields': ('user',)
        }),
        ("مشخصات فردی", {
            'fields': ('gender', 'age', 'bio', 'profile_picture')
        }),
    )
