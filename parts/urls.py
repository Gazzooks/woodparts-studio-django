from django.urls import path
from .views import PartListView, PartCreateView, PartUpdateView, PartDeleteView

app_name = 'parts'

urlpatterns = [
    path('', PartListView.as_view(), name='list'),
    path('add/', PartCreateView.as_view(), name='add'),
    path('<int:pk>/edit/', PartUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', PartDeleteView.as_view(), name='delete'),
    path('<int:project_id>/', PartListView.as_view(), name='manager'),
]