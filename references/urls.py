from django.urls import path
from . import views

app_name = 'references'  # This registers the namespace

urlpatterns = [
    path('wood-types/', views.WoodTypesView.as_view(), name='wood_types'),
    path('screw-chart/', views.ScrewChartView.as_view(), name='screw_chart'),
    path('nominal-actual/', views.NominalActualView.as_view(), name='nominal_actual'),
    path('joint-types/', views.JointTypesView.as_view(), name='joint_types'),
]
