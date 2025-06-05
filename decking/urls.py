from django.urls import path
from . import views

app_name = 'decking'

urlpatterns = [
    path('', views.deck_boards, name='deck_boards'),
    path('framing/', views.framing, name='framing'),
    path('footings/', views.footings, name='footings'),
]
