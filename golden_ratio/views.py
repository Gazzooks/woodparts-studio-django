# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

PHI = 1.61803398875

def get_tab_nav(active_tab):
    return '''
<ul class="nav nav-tabs mb-3">
    <li class="nav-item">
        <a class="nav-link {active1}" href="/golden-ratio/">Length Proportions</a>
    </li>
    <li class="nav-item">
        <a class="nav-link {active2}" href="/golden-ratio/golden-rectangle/">Golden Rectangle</a>
    </li>
</ul>
'''.format(
    active1="active" if active_tab == "length_proportions" else "",
    active2="active" if active_tab == "golden_rectangle" else ""
)

@login_required
def length_proportions(request):
    results = {}
    if request.method == 'POST':
        try:
            known_length = float(request.POST.get('known_length', 0))
            units = request.POST.get('units', 'inches')
            # A is longer, B is shorter, A+B is total
            # If known_length is A (longer)
            shorter_b = round(known_length / PHI, 3)
            total_ab = round(known_length + shorter_b, 3)
            # If known_length is B (shorter)
            longer_a = round(known_length * PHI, 3)
            total_ab_from_b = round(known_length + longer_a, 3)
            # If known_length is total (A+B)
            longer_a_from_total = round(known_length / PHI, 3)
            shorter_b_from_total = round(known_length - longer_a_from_total, 3)
            results = {
                'known_length': known_length,
                'units': units,
                'shorter_b': shorter_b,
                'total_ab': total_ab,
                'longer_a': longer_a,
                'total_ab_from_b': total_ab_from_b,
                'longer_a_from_total': longer_a_from_total,
                'shorter_b_from_total': shorter_b_from_total,
            }
        except Exception:
            results = {'error': 'Invalid input.'}
    context = {
        'active_tab': 'length_proportions',
        'results': results,
        'tab_nav': get_tab_nav('length_proportions')
    }
    return render(request, 'golden_ratio/length_proportions.html', context)

@login_required
def golden_rectangle(request):
    results = {}
    if request.method == 'POST':
        try:
            known_dim = request.POST.get('known_dim', 'width')
            value = float(request.POST.get('value', 0))
            units = request.POST.get('units', 'inches')
            if known_dim == 'width':
                width = value
                height = round(width / PHI, 3)
            else:
                height = value
                width = round(height * PHI, 3)
            area = round(width * height, 3)
            results = {
                'known_dim': known_dim,
                'value': value,
                'units': units,
                'width': width,
                'height': height,
                'area': area,
            }
        except Exception:
            results = {'error': 'Invalid input.'}
    context = {
        'active_tab': 'golden_rectangle',
        'results': results,
        'tab_nav': get_tab_nav('golden_rectangle')
    }
    return render(request, 'golden_ratio/golden_rectangle.html', context)
