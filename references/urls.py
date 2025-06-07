from django.urls import path
from . import views

app_name = 'references'

urlpatterns = [
    # Wood & Materials
    path('wood-types/', views.wood_types, name='wood_types'),
    path('nominal-actual-sizes/', views.nominal_actual_sizes, name='nominal_actual_sizes'),
    path('lumber-grades/', views.lumber_grades, name='lumber_grades'),
    path('material-properties/', views.material_properties, name='material_properties'),

    # Hardware & Fasteners
    path('screw-size-chart/', views.screw_size_chart, name='screw_size_chart'),
    path('bolt-nut-chart/', views.bolt_nut_chart, name='bolt_nut_chart'),
    path('nail-chart/', views.nail_chart, name='nail_chart'),
    path('hardware-catalog/', views.hardware_catalog, name='hardware_catalog'),

    # Joinery & Techniques
    path('joint-types/', views.joint_types, name='joint_types'),
    path('cutting-techniques/', views.cutting_techniques, name='cutting_techniques'),
    path('assembly-methods/', views.assembly_methods, name='assembly_methods'),

    # Finishing
    path('finishing-guide/', views.finishing_guide, name='finishing_guide'),
    path('stain-colors/', views.stain_colors, name='stain_colors'),
    path('finish-compatibility/', views.finish_compatibility, name='finish_compatibility'),

    # Standalone references
    path('documentation/', views.documentation, name='documentation'),
    path('quick-reference-cards/', views.quick_reference_cards, name='quick_reference_cards'),
    path('safety-guidelines/', views.safety_guidelines, name='safety_guidelines'),
]
