# parts/urls.py
from django.urls import path
from . import views

app_name = 'parts'  # Add this line

urlpatterns = [
    path('manager/', views.PartsManagerView.as_view(), name='manager'),
    path('add/', views.add_part_ajax, name='add'),
    path('<int:pk>/edit/', views.PartUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.PartDeleteView.as_view(), name='delete'),
]
