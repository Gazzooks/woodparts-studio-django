from django.shortcuts import render

def wood_types(request):
    return render(request, 'references/wood_types.html')

def nominal_actual_sizes(request):
    return render(request, 'references/nominal_actual_sizes.html')

def lumber_grades(request):
    return render(request, 'references/lumber_grades.html')

def material_properties(request):
    return render(request, 'references/material_properties.html')

def screw_size_chart(request):
    return render(request, 'references/screw_size_chart.html')

def bolt_nut_chart(request):
    return render(request, 'references/bolt_nut_chart.html')

def nail_chart(request):
    return render(request, 'references/nail_chart.html')

def hardware_catalog(request):
    return render(request, 'references/hardware_catalog.html')

def joint_types(request):
    return render(request, 'references/joint_types.html')

def cutting_techniques(request):
    return render(request, 'references/cutting_techniques.html')

def assembly_methods(request):
    return render(request, 'references/assembly_methods.html')

def finishing_guide(request):
    return render(request, 'references/finishing_guide.html')

def stain_colors(request):
    return render(request, 'references/stain_colors.html')

def finish_compatibility(request):
    return render(request, 'references/finish_compatibility.html')

def documentation(request):
    return render(request, 'references/documentation.html')

def quick_reference_cards(request):
    return render(request, 'references/quick_reference_cards.html')

def safety_guidelines(request):
    return render(request, 'references/safety_guidelines.html')
