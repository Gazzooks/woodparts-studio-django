from django.urls import path
from . import views

app_name = "shop_assets"

urlpatterns = [
    # Main manager page (shows both tabs)
    path('', views.manager, name='manager'),

    # Tools CRUD
    path('tools/add/', views.add_tool, name='add_tool'),
    path('tools/<int:pk>/edit/', views.edit_tool, name='edit_tool'),
    path('tools/<int:pk>/delete/', views.delete_tool, name='delete_tool'),

    # Maintenance CRUD
    path('maintenance/add/', views.add_maintenance, name='add_maintenance'),
    path('maintenance/<int:pk>/edit/', views.edit_maintenance, name='edit_maintenance'),
    path('maintenance/<int:pk>/delete/', views.delete_maintenance, name='delete_maintenance'),

    # (Optional) Export/Import endpoints
    path('tools/export/', views.export_tools, name='export_tools'),
    path('tools/import/', views.import_tools, name='import_tools'),
    path('maintenance/import/', views.import_maintenance, name='import_maintenance'),
    path('maintenance/export/', views.export_maintenance, name='export_maintenance'),
]
