# calculators/urls.py
from .views import board_foot_calculator, fraction_calculator
from django.urls import path

app_name = 'calculators'

urlpatterns = [
    path('board-foot/', board_foot_calculator, name='board_foot'),
    path('fraction/', fraction_calculator, name='fraction'),
]
