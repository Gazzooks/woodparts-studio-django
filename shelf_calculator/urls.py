from django.urls import path
from .views import shelf_calculator

app_name = 'shelf_calculator'

urlpatterns = [
    path('', shelf_calculator, name='shelf'),
]
