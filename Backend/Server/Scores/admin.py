from django.contrib import admin
from .models import ServiceScore


@admin.register(ServiceScore)
class ServiceScoreAdmin(admin.ModelAdmin):
    list_display = ('service', 'quality', 'behavior', 'time', 'overall', 'created_at')
    search_fields = ('service__title',)
    readonly_fields = ('overall', 'created_at')
