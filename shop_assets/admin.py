from django.contrib import admin
from .models import Tool, ToolMaintenance

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'brand', 'model', 'location', 'purchase_date')

@admin.register(ToolMaintenance)
class ToolMaintenanceAdmin(admin.ModelAdmin):
    list_display = ('tool', 'maintenance_date', 'maintenance_type')
