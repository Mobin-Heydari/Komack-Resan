from django.contrib import admin
from django.utils import timezone
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
    CompanyAddress,
    CompanyCard,
)

# -------------------------------
# Inline Admin Classes
# -------------------------------

class WorkDayInline(admin.TabularInline):
    model = WorkDay
    extra = 0
    readonly_fields = ('time_range',)
    verbose_name = "روز کاری"
    verbose_name_plural = "روزهای کاری"


class CompanyFirstItemInline(admin.TabularInline):
    model = CompanyFirstItem
    extra = 0
    verbose_name = "آیتم اول"
    verbose_name_plural = "آیتم‌های اول شرکت"


class CompanySecondItemInline(admin.TabularInline):
    model = CompanySecondItem
    extra = 0
    verbose_name = "آیتم دوم"
    verbose_name_plural = "آیتم‌های دوم شرکت"


class CompanyEmployeeInline(admin.TabularInline):
    model = CompanyEmployee
    extra = 0
    verbose_name = "کارمند"
    verbose_name_plural = "کارمندها"


class CompanyValidationStatusInline(admin.StackedInline):
    model = CompanyValidationStatus
    extra = 0
    can_delete = False
    verbose_name = "وضعیت تایید شرکت"
    verbose_name_plural = "وضعیت تایید شرکت"


class CompanyAddressInline(admin.StackedInline):
    model = CompanyAddress
    extra = 0
    verbose_name = "آدرس شرکت"
    verbose_name_plural = "آدرس های شرکت"


class CompanyCardInline(admin.StackedInline):
    model = CompanyCard
    extra = 0
    verbose_name = "کارت شرکت"
    verbose_name_plural = "کارت‌های شرکت"

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
    icon_preview.short_description = "پیش نمایش آیکون"


@admin.register(SecondItem)
class SecondItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon_preview')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}

    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="50" height="50" />', obj.icon.url)
        return "-"
    icon_preview.short_description = "پیش نمایش آیکون"


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'employer',
        'industry',
        'service_type',
        'is_validated',
        'is_off_season',
        'overall_score_display',
        'created_at',
        'logo_preview',
    )
    search_fields = ('name', 'employer__username', 'industry__name')
    list_filter = ('is_validated', 'is_off_season', 'industry', 'service_type')
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ('created_at', 'updated_at', 'logo_preview', 'banner_preview')
    
    fieldsets = (
        ("مشخصات اصلی", {
            'fields': ('employer', 'industry', 'name', 'slug', 'description', 'service_type')
        }),
        ("اطلاعات تماس", {
            'fields': ('website', 'email', 'phone_number', 'postal_code')
        }),
        ("شبکه‌های اجتماعی", {
            'fields': ('linkedin', 'twitter', 'instagram')
        }),
        ("تصاویر و ویدئو", {
            'fields': ('logo', 'logo_preview', 'banner', 'banner_preview', 'intro_video')
        }),
        ("اطلاعات تکمیلی", {
            'fields': ('founded_date',)
        }),
        ("وضعیت", {
            'fields': ('is_validated', 'is_off_season')
        }),
        ("تاریخ‌ها", {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    inlines = [
        WorkDayInline,
        CompanyFirstItemInline,
        CompanySecondItemInline,
        CompanyEmployeeInline,
        CompanyValidationStatusInline,
        CompanyAddressInline,
        CompanyCardInline,
    ]
    
    def overall_score_display(self, obj):
        score = obj.overall_score
        if score is not None:
            return f"{score:.2f}"
        return "ندارد"
    overall_score_display.short_description = "امتیاز کلی"
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" height="50" />', obj.logo.url)
        return "ندارد"
    logo_preview.short_description = "پیش نمایش لوگو"
    
    def banner_preview(self, obj):
        if obj.banner:
            return format_html('<img src="{}" width="100" height="50" />', obj.banner.url)
        return "ندارد"
    banner_preview.short_description = "پیش نمایش بنر"



@admin.register(CompanyValidationStatus)
class CompanyValidationStatusAdmin(admin.ModelAdmin):
    list_display = (
        'company',
        'overall_status',
        'business_license_status_display',
        'validated_by',
        'validated_at'
    )
    search_fields = ('company__name',)
    list_filter = ('overall_status',)
    readonly_fields = ('created_at', 'updated_at',)

    def business_license_status_display(self, obj):
        return "تایید شده" if obj.business_license_status else "تایید نشده"
    business_license_status_display.short_description = "وضعیت جواز کسب"


@admin.register(CompanyEmployee)
class CompanyEmployeeAdmin(admin.ModelAdmin):
    list_display = ('company', 'employee', 'position', 'created_at')
    search_fields = ('employee__username', 'company__name')
    list_filter = ('position', 'company')
    readonly_fields = ('created_at', 'updated_at',)


@admin.register(WorkDay)
class WorkDayAdmin(admin.ModelAdmin):
    list_display = ('company', 'day_of_week', 'time_range', 'is_closed')
    search_fields = ('company__name',)
    list_filter = ('company', 'day_of_week', 'is_closed')


@admin.register(CompanyFirstItem)
class CompanyFirstItemAdmin(admin.ModelAdmin):
    list_display = ('first_item', 'compay')
    search_fields = ('first_item__name', 'compay__name')


@admin.register(CompanySecondItem)
class CompanySecondItemAdmin(admin.ModelAdmin):
    list_display = ('second_item', 'compay')
    search_fields = ('second_item__name', 'compay__name')


@admin.register(CompanyAddress)
class CompanyAddressAdmin(admin.ModelAdmin):
    list_display = ('company', 'city', 'address', 'created_at')
    search_fields = ('company__name', 'city__name', 'address')
    readonly_fields = ('created_at', 'updated_at',)


@admin.register(CompanyCard)
class CompanyCardAdmin(admin.ModelAdmin):
    list_display = ('company', 'card_number', 'expiration_date', 'card_holder_name', 'created_at')
    search_fields = ('company__name', 'card_number', 'card_holder_name')
    readonly_fields = ('created_at', 'updated_at',)
