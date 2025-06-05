from django.urls import path
from .views import wall_panels_calculator

app_name = 'wall_panels'
urlpatterns = [
    path('', wall_panels_calculator, name='calculator'),
]
