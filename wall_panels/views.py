from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def wall_panels_calculator(request):
    wall_area = None
    num_panels = None
    panel_coverage = None
    error_msg = None
    user_prefers_metric = False

    if hasattr(request.user, 'userpreferences'):
        user_prefers_metric = (request.user.userpreferences.default_units == 'metric')

    if request.method == 'POST':
        try:
            wall_width = float(request.POST.get('wall_width', 0))
            wall_height = float(request.POST.get('wall_height', 0))
            panel_width = float(request.POST.get('panel_width', 0))
            panel_height = float(request.POST.get('panel_height', 0))
            waste_percentage = float(request.POST.get('waste_percentage', 0))
            exclude_openings = request.POST.get('exclude_openings') == 'on'
            num_openings = int(request.POST.get('num_openings', 0))
            avg_opening_area = float(request.POST.get('avg_opening_area', 0))

            if user_prefers_metric:
                wall_area = wall_width * wall_height  # m²
                panel_width_m = panel_width / 1000
                panel_height_m = panel_height / 1000
                panel_coverage = panel_width_m * panel_height_m  # m²
                if not exclude_openings and num_openings > 0 and avg_opening_area > 0:
                    total_opening_area = num_openings * avg_opening_area
                    if total_opening_area >= wall_area:
                        error_msg = "Total opening area exceeds or matches wall area. Please check your inputs."
                        wall_area = 0
                    else:
                        wall_area -= total_opening_area
            else:
                wall_area = wall_width * wall_height  # sq ft
                panel_width_ft = panel_width / 12
                panel_height_ft = panel_height / 12
                panel_coverage = panel_width_ft * panel_height_ft  # sq ft
                if not exclude_openings and num_openings > 0 and avg_opening_area > 0:
                    total_opening_area = num_openings * avg_opening_area
                    if total_opening_area >= wall_area:
                        error_msg = "Total opening area exceeds or matches wall area. Please check your inputs."
                        wall_area = 0
                    else:
                        wall_area -= total_opening_area

            wall_area = max(wall_area, 0)
            if panel_coverage > 0 and wall_area > 0:
                panels_needed = wall_area / panel_coverage
                panels_needed *= (1 + waste_percentage / 100)
                num_panels = int(-(-panels_needed // 1))
            else:
                num_panels = 0

        except (ValueError, TypeError):
            wall_area = None
            num_panels = None
            panel_coverage = None
            error_msg = "Invalid input. Please check your values."

    return render(request, 'wall_panels/calculator.html', {
        'wall_area': wall_area,
        'num_panels': num_panels,
        'panel_coverage': panel_coverage,
        'user_prefers_metric': user_prefers_metric,
        'error_msg': error_msg,
    })
