from django.urls import path
from .views import DashboardView,ProjectDashboardView, ProjectListView, ProjectDetailView
from . import views

app_name = 'projects'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    # Alternative route for dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard_alt'),
    path('list/', ProjectListView.as_view(), name='list'),
    path('create/', views.ProjectCreateView.as_view(), name='create'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='detail'),
    # Add other project-related URLs here
]
