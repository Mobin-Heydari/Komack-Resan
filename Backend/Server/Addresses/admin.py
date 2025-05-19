from django.contrib import admin
from .models import Province, City, RecipientAddress




# Inline for editing cities directly in the Province admin.
class CityInline(admin.TabularInline):
    model = City
    extra = 1
    fields = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}
    verbose_name = "شهر"
    verbose_name_plural = "شهرها"


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'number_of_cities')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [CityInline]

    def number_of_cities(self, obj):
        return obj.city_set.count()
    number_of_cities.short_description = "تعداد شهرها"


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'slug')
    search_fields = ('name', 'province__name')
    list_filter = ('province',)
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ('province',)


@admin.register(RecipientAddress)
class RecipientAddressAdmin(admin.ModelAdmin):
    list_display = ('title', 'Recipient', 'city', 'address', 'created_at')
    search_fields = ('title', 'address', 'Recipient__username', 'city__name')
    list_filter = ('city', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ('Recipient', 'city')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ("مشخصات گیرنده", {
            'fields': ('Recipient', 'title')
        }),
        ("مکان", {
            'fields': ('city', 'address')
        }),
        ("تاریخ ثبت", {
            'fields': ('created_at', 'updated_at')
        }),
    )
