# calculators/urls.py
from django.urls import path
from . import views

app_name = 'calculators'

urlpatterns = [
    path('board-foot/', views.board_foot_calculator, name='board_foot'),
    path('fraction/', views.fraction_calculator, name='fraction'),
]
