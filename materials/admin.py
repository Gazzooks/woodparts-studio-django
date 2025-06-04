# materials/admin.py
from django.contrib import admin
from .models import StockMaterial

class StockMaterialAdmin(admin.ModelAdmin):
    search_fields = ['material']  # Match your model field name
    # ... other configurations ...

admin.site.register(StockMaterial, StockMaterialAdmin)
