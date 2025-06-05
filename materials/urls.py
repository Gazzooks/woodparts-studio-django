from django.urls import path
from .views import MaterialListView, MaterialCreateView, MaterialDetailView, MaterialUpdateView, MaterialDeleteView, MaterialDuplicateView

app_name = 'materials'  # Critical namespace declaration

urlpatterns = [
    path('', MaterialListView.as_view(), name='list'),
    path('create/', MaterialCreateView.as_view(), name='create'),
    path('<int:pk>/', MaterialDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', MaterialUpdateView.as_view(), name='edit'),
    path('<int:pk>/duplicate/', MaterialDuplicateView.as_view(), name='duplicate'),
    path('<int:pk>/delete/', MaterialDeleteView.as_view(), name='delete'),
]
