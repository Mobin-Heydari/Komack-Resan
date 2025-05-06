from django.contrib import admin
from django.utils.html import format_html
from .models import (
    FirstItem,
    SecondItem,
    Company,
    CompanyValidationStatus,
    CompanyEmployee,
    WorkDay,
    CompanyFirstItem,
    CompanySecondItem,
)

# -------------------------------
# Inline Admin Classes
# -------------------------------

class WorkDayInline(admin.TabularInline):
    model = WorkDay
    extra = 0
    # Optionally, you can display a readonly field for the computed time_range
    readonly_fields = ('time_range',)


class CompanyFirstItemInline(admin.TabularInline):
    model = CompanyFirstItem
    extra = 0


class CompanySecondItemInline(admin.TabularInline):
    model = CompanySecondItem
    extra = 0


class CompanyEmployeeInline(admin.TabularInline):
    model = CompanyEmployee
    extra = 0


class CompanyValidationStatusInline(admin.StackedInline):
    model = CompanyValidationStatus
    extra = 0
    # Hide validation status if you prefer (and manage it separately)
    can_delete = False


# -------------------------------
# Model Admin Classes
# -------------------------------

@admin.register(FirstItem)
class FirstItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon_preview')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    
    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="50" height="50" />', obj.icon.url)
        return "-"
    icon_preview.short_description = "Icon Preview"


@admin.register(SecondItem)
class SecondItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon_preview')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    
    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="50" height="50" />', obj.icon.url)
        return "-"
    icon_preview.short_description = "Icon Preview"


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'name', 
        'employer', 
        'industry', 
        'is_validated', 
        'is_off_season', 
        'created_at'
    )
    search_fields = ('name', 'employer__username', 'industry__name')
    list_filter = ('is_validated', 'is_off_season', 'industry')
    prepopulated_fields = {"slug": ("name",)}
    inlines = [
        WorkDayInline,
        CompanyFirstItemInline,
        CompanySecondItemInline,
        CompanyEmployeeInline,
        CompanyValidationStatusInline,
    ]


@admin.register(CompanyValidationStatus)
class CompanyValidationStatusAdmin(admin.ModelAdmin):
    list_display = (
        'company', 
        'overall_status', 
        'business_license_status', 
        'validated_by', 
        'validated_at'
    )
    search_fields = ('company__name',)
    list_filter = ('overall_status',)


@admin.register(CompanyEmployee)
class CompanyEmployeeAdmin(admin.ModelAdmin):
    list_display = ('company', 'employee', 'position', 'created_at')
    search_fields = ('employee__username', 'company__name')
    list_filter = ('position', 'company')


@admin.register(WorkDay)
class WorkDayAdmin(admin.ModelAdmin):
    list_display = ('company', 'day_of_week', 'time_range', 'is_closed')
    search_fields = ('company__name',)
    list_filter = ('company', 'day_of_week')


@admin.register(CompanyFirstItem)
class CompanyFirstItemAdmin(admin.ModelAdmin):
    list_display = ('first_item', 'compay')
    search_fields = ('first_item__name', 'compay__name')


@admin.register(CompanySecondItem)
class CompanySecondItemAdmin(admin.ModelAdmin):
    list_display = ('second_item', 'compay')
    search_fields = ('second_item__name', 'compay__name')
