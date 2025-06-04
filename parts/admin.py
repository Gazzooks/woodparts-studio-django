from django.contrib import admin
from .models import Part
from projects.models import Project
from materials.models import StockMaterial

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    # Date-based navigation
    date_hierarchy = 'date_created'
    
    # List display configuration
    list_display = (
        'name', 
        'project', 
        'material',
        'quantity',
        'date_created',
        'date_updated'
    )
    
    # Filtering options
    list_filter = (
        'project',
        'material',
        ('date_created', admin.DateFieldListFilter),
    )
    
    # Search capabilities
    search_fields = (
        'name',
        'project__name',
        'material__name',
        'notes'
    )
    
    # Form configuration
    fieldsets = (
        (None, {
            'fields': (
                'name', 
                'project', 
                'material',
                'quantity',
                'notes'
            )
        }),
        ('Dimensions', {
            'fields': (
                ('length', 'width', 'thickness'),
            )
        }),
        ('Timestamps', {
            'fields': (
                'date_created',
                'date_updated'
            ),
            'classes': ('collapse',)
        }),
    )
    
    # Automatic read-only for timestamps
    readonly_fields = ('date_created', 'date_updated')

    # Related field optimizations
    autocomplete_fields = ['project', 'material']
    raw_id_fields = ('project',)

    # List customization
    list_per_page = 50
    list_max_show_all = 200
    show_full_result_count = False
    preserve_filters = True

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'project', 
            'material'
        )

