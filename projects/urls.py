from django.urls import path
from .views import (
    DashboardView,
    ProjectListView,
    ProjectCreateView,
    ProjectDetailView,
    ProjectUpdateView,
    ProjectDeleteView,
    set_current_project,
    close_current_project,
)

app_name = 'projects'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('list/', ProjectListView.as_view(), name='list'),
    path('create/', ProjectCreateView.as_view(), name='create'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', ProjectUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', ProjectDeleteView.as_view(), name='delete'),
    path('set-current/<int:pk>/', set_current_project, name='set_current_project'),
    path('close-current/', close_current_project, name='close_current_project'),
]
