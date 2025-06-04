# projects/admin.py
from django.contrib import admin
from .models import Project, ProjectSettings

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'datecreated', 'datemodified', 'status', 'owner')
    list_filter = ('status', 'datecreated', 'datemodified', 'owner')
    date_hierarchy = 'datecreated'
    ordering = ('-datemodified',)
    search_fields = ('name', 'description', 'owner__username')

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'status', 'owner', 'notes')
        }),
        ('Metadata', {
            'fields': ('datecreated', 'datemodified'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('datecreated', 'datemodified')

@admin.register(ProjectSettings)
class ProjectSettingsAdmin(admin.ModelAdmin):
    autocomplete_fields = ['project']
    list_display = ('project', 'measurement_units', 'cut_optimization_enabled')
