from django.contrib import admin
from django.utils.html import format_html
from .models import IndustryCategory, Industry



# Inline for managing industries directly in an IndustryCategory's change view.
class IndustryInline(admin.TabularInline):
    model = Industry
    extra = 0
    fields = ('name', 'slug', 'icon_preview', 'price_per_service')
    readonly_fields = ('icon_preview',)
    
    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="50" height="50" alt="{}" />', obj.icon.url, obj.name)
        return "-"
    icon_preview.short_description = "پیش نمایش آیکون"

@admin.register(IndustryCategory)
class IndustryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon_preview', 'industries_count')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [IndustryInline]
    
    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="50" height="50" alt="{}" />', obj.icon.url, obj.name)
        return "-"
    icon_preview.short_description = "پیش نمایش آیکون"
    
    def industries_count(self, obj):
        return obj.industries.count()
    industries_count.short_description = "تعداد صنایع"


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'price_per_service', 'icon_preview')
    search_fields = ('name',)
    list_filter = ('category',)
    prepopulated_fields = {"slug": ("name",)}
    
    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="50" height="50" alt="{}" />', obj.icon.url, obj.name)
        return "-"
    icon_preview.short_description = "پیش نمایش آیکون"
