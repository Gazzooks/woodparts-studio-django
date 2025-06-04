from django.urls import path
from .views import (
    DashboardView,
    ProjectListView,
    ProjectCreateView,
    ProjectDetailView, ProjectUpdateView, ProjectDeleteView
)

app_name = 'projects'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('dashboard/', DashboardView.as_view(), name='dashboard_alt'),
    path('list/', ProjectListView.as_view(), name='list'),
    path('create/', ProjectCreateView.as_view(), name='create'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', ProjectUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', ProjectDeleteView.as_view(), name='delete'),
]
