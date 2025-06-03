from django.urls import path
from . import views

app_name = 'cutlists'

urlpatterns = [
    # cutlists/urls.py
    path('create/<int:project_id>/', views.CutlistCreateView.as_view(), name='creator')

]
