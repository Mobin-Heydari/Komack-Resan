from django.contrib import admin
from django.utils.html import format_html
from .models import Industry, IndustryCategory


class IndustryInline(admin.TabularInline):
    model = Industry
    extra = 0
    fields = ('name', 'price_per_service', 'icon_preview')
    readonly_fields = ('icon_preview',)

    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="50" height="50" />', obj.icon.url)
        return "-"
    icon_preview.short_description = "آیکون"


@admin.register(IndustryCategory)
class IndustryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon_preview')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [IndustryInline]

    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="50" height="50" />', obj.icon.url)
        return "-"
    icon_preview.short_description = "آیکون"


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'price_per_service', 'icon_preview')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)
    prepopulated_fields = {"slug": ("name",)}

    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="50" height="50" />', obj.icon.url)
        return "-"
    icon_preview.short_description = "آیکون"
