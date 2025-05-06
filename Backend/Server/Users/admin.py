from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, IdCardInFormation



# ------------------------------------------------------------------------------
# IdCardInFormation Admin
# ------------------------------------------------------------------------------

class IdCardInFormationAdmin(admin.ModelAdmin):
    list_display = ('id_card_number', 'id_card_status', 'preview')
    search_fields = ('id_card_number',)
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.id_card:
            # Provide a link to view the file in a new tab
            return format_html('<a href="{}" target="_blank">View ID Card</a>', obj.id_card.url)
        return "No Card"
    preview.short_description = "ID Card Preview"


# ------------------------------------------------------------------------------
# Custom User Admin
# ------------------------------------------------------------------------------

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'full_name', 'email', 'phone', 'user_type', 'status', 'joined_date', 'is_active', 'is_admin')
    list_filter = ('user_type', 'status', 'is_active')
    search_fields = ('username', 'full_name', 'email', 'phone')
    ordering = ('joined_date',)
    readonly_fields = ('last_updated', 'joined_date')

    # Fieldsets for changing user details
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal Info', {'fields': ('username', 'full_name', 'email', 'id_card_info')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'user_type', 'status', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('joined_date', 'last_updated')}),
    )

    # Fieldsets for creating a new user (on the add form)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'username', 'email', 'full_name', 'user_type', 'status', 'password1', 'password2'),
        }),
    )


# ------------------------------------------------------------------------------
# Register Admin Classes
# ------------------------------------------------------------------------------

admin.site.register(User, UserAdmin)
admin.site.register(IdCardInFormation, IdCardInFormationAdmin)
