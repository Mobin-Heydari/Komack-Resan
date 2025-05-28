from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User



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
        ("اطلاعات شخصی", {'fields': ('full_name',)}),
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

admin.site.register(User, UserAdmin)
