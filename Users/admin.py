from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, IdCardInFormation

# Customize the admin site's header and titles in Persian.
admin.site.site_header = "پنل مدیریت"
admin.site.site_title = "پنل مدیریت"
admin.site.index_title = "خوش آمدید به پنل مدیریت"

# Admin for the IdCardInFormation model
class IdCardInFormationAdmin(admin.ModelAdmin):
    list_display = (
        'id_card_number', 
        'get_id_card_status_display', 
        'id_card_preview'
    )
    list_filter = ('id_card_status',)
    search_fields = ('id_card_number',)
    
    def id_card_preview(self, obj):
        """
        Returns a clickable link to the uploaded id_card file.
        """
        if obj.id_card:
            return format_html('<a href="{}" target="_blank">مشاهده</a>', obj.id_card.url)
        return "فاقد فایل"
    id_card_preview.short_description = 'پیش نمایش کارت ملی'

admin.site.register(IdCardInFormation, IdCardInFormationAdmin)


# Custom admin for the User model
class UserAdmin(BaseUserAdmin):
    readonly_fields = ('joined_date', 'last_updated')  # Fields generated automatically; display as read-only.
    
    list_display = (
        'username', 
        'full_name', 
        'email', 
        'phone', 
        'user_type', 
        'status', 
        'id_card_details',
        'joined_date', 
        'is_admin'
    )
    list_filter = ('user_type', 'status', 'is_admin', 'joined_date')
    search_fields = ('username', 'full_name', 'email', 'phone')
    ordering = ('joined_date',)
    date_hierarchy = 'joined_date'
    filter_horizontal = ('groups', 'user_permissions',)
    
    # Define fieldsets for the change (edit) view with Persian labels.
    fieldsets = (
        ("اطلاعات ورود", {'fields': ('phone', 'username', 'email', 'password')}),
        ("اطلاعات شخصی", {'fields': ('full_name', 'id_card_info')}),
        ("سطح دسترسی", {'fields': ('is_admin', 'is_active')}),
        ("نوع و وضعیت کاربر", {'fields': ('user_type', 'status')}),
        ("تاریخ‌های مهم", {'fields': ('joined_date', 'last_updated')}),
    )
    
    # Define the fields used for creating a new user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'phone', 
                'username', 
                'email', 
                'full_name', 
                'user_type', 
                'status', 
                'password1', 
                'password2'
            ),
        }),
    )
    
    def id_card_details(self, obj):
        """
        Returns a combined descriptive string for the user's associated
        IdCardInFormation instance, including the national ID number and its status.
        """
        if obj.id_card_info:
            id_number = obj.id_card_info.id_card_number or "فاقد شماره ملی"
            status = obj.id_card_info.get_id_card_status_display()
            return f"{id_number} - {status}"
        return "ندارد"
    id_card_details.short_description = "اطلاعات کارت ملی"

admin.site.register(User, UserAdmin)
