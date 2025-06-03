from django.urls import path
from .views import length_converter, fraction_converter

app_name = 'converters'

urlpatterns = [
    path('length/', length_converter, name='length'),
    path('fraction/', fraction_converter, name='fraction'),
]