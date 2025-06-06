from django.urls import path
from . import views

app_name = 'golden_ratio'

urlpatterns = [
    path('', views.length_proportions, name='length_proportions'),
    path('golden-rectangle/', views.golden_rectangle, name='golden_rectangle'),
]
