from django.urls import path
from . import views

app_name = 'fraction_decimal_mm'

urlpatterns = [
    path('', views.fraction_to_decimal_mm, name='fraction_to_decimal_mm'),
    path('decimal-to-fraction/', views.decimal_to_fraction, name='decimal_to_fraction'),
    path('mm-to-fraction-decimal/', views.mm_to_fraction_decimal, name='mm_to_fraction_decimal'),
]
