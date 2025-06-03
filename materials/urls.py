from django.urls import path
from . import views

app_name = 'materials'  # Critical namespace declaration

urlpatterns = [
    path('', views.MaterialListView.as_view(), name='list'),
    path('add/', views.MaterialCreateView.as_view(), name='add'),
    path('<int:pk>/', views.MaterialDetailView.as_view(), name='detail'),
]
