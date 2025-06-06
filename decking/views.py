from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import math

@login_required
def deck_boards(request):
    results = {}
    user_prefers_metric = False

    if hasattr(request.user, 'userpreferences'):
        user_prefers_metric = (request.user.userpreferences.default_units == 'metric')

    if request.method == 'POST':
        try:
            deck_shape = request.POST.get('deck_shape', 'rectangular')
            results['deck_shape'] = deck_shape

            if deck_shape == 'custom':
                total_area_str = request.POST.get('total_area')
                if not total_area_str:
                    raise ValueError('Total area is required for custom shape.')
                total_area = float(total_area_str)
                length = width = 0  # Not used for custom shape
            else:
                length = float(request.POST.get('length', 0))
                width = float(request.POST.get('width', 0))
                total_area = 0  # Not used for rectangular shape

            board_width = float(request.POST.get('board_width', 5.5))
            board_length = float(request.POST.get('board_length', 16))
            gap = float(request.POST.get('gap', 0.25))
            waste = float(request.POST.get('waste_percentage', 10))
            direction = request.POST.get('board_direction', 'length')

            # Handle board width and gap based on user's unit preference
            if user_prefers_metric:
                board_width_m = board_width / 1000
                gap_m = gap / 1000
                effective_width = board_width_m + gap_m
            else:
                board_width_ft = board_width / 12
                gap_ft = gap / 12
                effective_width = board_width_ft + gap_ft

            # Calculate deck area
            if deck_shape == 'custom':
                deck_area = total_area
            else:
                deck_area = length * width

            # Determine number of boards and total linear length
            if deck_shape == 'custom':
                # For custom, assume a square shape for calculation
                assumed_width = math.sqrt(deck_area)
                num_boards = math.ceil(assumed_width / effective_width)
                total_length = assumed_width * num_boards
            else:
                if direction == 'length':
                    num_boards = math.ceil(width / effective_width)
                    total_length = length * num_boards
                else:
                    num_boards = math.ceil(length / effective_width)
                    total_length = width * num_boards

            # Adjust for waste
            total_length *= (1 + waste / 100)
            boards_needed = math.ceil(total_length / board_length)

            # Convert to metric for display if user prefers metric
            if user_prefers_metric:
                results.update({
                    'deck_area': deck_area,
                    'deck_area_unit': 'm²',
                    'boards_needed': boards_needed,
                    'board_width': board_width,
                    'board_width_unit': 'mm',
                    'board_length': board_length,
                    'board_length_unit': 'm',
                    'total_linear_feet': total_length,
                    'total_linear_feet_unit': 'm',
                    'gap': gap,
                    'gap_unit': 'mm',
                    'length': length,
                    'width': width,
                    'total_area': total_area,
                })
            else:
                results.update({
                    'deck_area': deck_area,
                    'deck_area_unit': 'sq ft',
                    'boards_needed': boards_needed,
                    'board_width': board_width,
                    'board_width_unit': 'in',
                    'board_length': board_length,
                    'board_length_unit': 'ft',
                    'total_linear_feet': total_length,
                    'total_linear_feet_unit': 'ft',
                    'gap': gap,
                    'gap_unit': 'in',
                    'length': length,
                    'width': width,
                    'total_area': total_area,
                })
        except ValueError as e:
            results = {'error': str(e) if str(e) else 'Invalid input. Please check your values.', 'deck_shape': deck_shape}
        except Exception as e:
            results = {'error': 'An error occurred. Please try again.', 'deck_shape': deck_shape}

    else:
        results = {'deck_shape': 'rectangular'}

    context = {
        'active_tab': 'deck_boards',
        'results': results,
        'user_prefers_metric': user_prefers_metric,
    }
    return render(request, 'decking/deck_boards.html', context)

@login_required
def framing(request):
    results = {}
    user_prefers_metric = False

    if hasattr(request.user, 'userpreferences'):
        user_prefers_metric = (request.user.userpreferences.default_units == 'metric')

    if request.method == 'POST':
        try:
            # Deck dimensions
            length = float(request.POST.get('length', 0))
            width = float(request.POST.get('width', 0))
            joist_spacing = float(request.POST.get('joist_spacing', 16))
            beam_span = float(request.POST.get('beam_span', 3.66 if user_prefers_metric else 12))
            waste = float(request.POST.get('waste_percentage', 10))

            # Convert joist spacing to meters if user prefers metric (input is in mm)
            if user_prefers_metric:
                joist_spacing_m = joist_spacing / 1000  # mm to meters
            else:
                joist_spacing_in = joist_spacing  # inches
                joist_spacing_m = joist_spacing_in * 0.0254  # inches to meters (for calculation if needed)

            # Number of joists: (width / spacing) + 1, round up
            # For imperial, joist_spacing is in inches, so convert width to inches if needed
            # For metric, joist_spacing is in meters (already converted)
            if user_prefers_metric:
                # All inputs are in meters
                num_joists = math.ceil(width / joist_spacing_m) + 1
            else:
                # Convert width to inches for calculation
                width_in = width * 12
                num_joists = math.ceil(width_in / joist_spacing_in) + 1

            # Beam length: number of beams = (length / beam_span) + 1, round up, then total beam length
            num_beams = math.ceil(length / beam_span) + 1
            beam_length = num_beams * width

            # Rim joist length: 2 * (length + width)
            rim_joist_length = 2 * (length + width)

            # Adjust for waste
            beam_length *= (1 + waste / 100)
            rim_joist_length *= (1 + waste / 100)

            # Convert to metric for display if user prefers metric
            if user_prefers_metric:
                results.update({
                    'num_joists': num_joists,
                    'beam_length': beam_length,
                    'beam_length_unit': 'm',
                    'rim_joist_length': rim_joist_length,
                    'rim_joist_length_unit': 'm',
                    'length': length,
                    'width': width,
                    'joist_spacing': joist_spacing,
                    'beam_span': beam_span,
                    'waste_percentage': waste,
                })
            else:
                results.update({
                    'num_joists': num_joists,
                    'beam_length': beam_length,
                    'beam_length_unit': 'ft',
                    'rim_joist_length': rim_joist_length,
                    'rim_joist_length_unit': 'ft',
                    'length': length,
                    'width': width,
                    'joist_spacing': joist_spacing,
                    'beam_span': beam_span,
                    'waste_percentage': waste,
                })
        except Exception as e:
            results = {'error': 'Invalid input. Please check your values.'}

    context = {
        'active_tab': 'framing',
        'results': results,
        'user_prefers_metric': user_prefers_metric,
    }
    return render(request, 'decking/framing.html', context)

@login_required
def footings(request):
    results = {}
    user_prefers_metric = False

    if hasattr(request.user, 'userpreferences'):
        user_prefers_metric = (request.user.userpreferences.default_units == 'metric')

    if request.method == 'POST':
        try:
            # Get form data
            deck_area = float(request.POST.get('deck_area', 0))
            beam_length = float(request.POST.get('beam_length', 0))
            post_spacing = float(request.POST.get('post_spacing', 2.44 if user_prefers_metric else 8))
            num_beams = int(request.POST.get('num_beams', 1))
            footing_diameter = float(request.POST.get('footing_diameter', 305 if user_prefers_metric else 12))
            footing_depth = float(request.POST.get('footing_depth', 1.22 if user_prefers_metric else 4))
            bag_size = float(request.POST.get('concrete_bag_size', 20 if user_prefers_metric else 40))

            # Number of footings: (beam length / post spacing +1) * number of beams, rounded up.
            # This places a footing at each end and at each interval, as is standard practice
            num_footings = math.ceil((beam_length / post_spacing + 1) * num_beams)

            # Volume per footing (cylinder): π * r^2 * h
            radius = footing_diameter / 2
            if user_prefers_metric:
                # All in meters
                radius_m = radius / 1000  # mm to meters
                depth_m = footing_depth
                volume_per_footing = math.pi * (radius_m ** 2) * depth_m  # cubic meters per footing
                total_concrete = volume_per_footing * num_footings  # cubic meters total
                bag_coverage = {20: 0.013, 25: 0.016, 40: 0.026}.get(bag_size, 0.013)  # cubic meters per bag
            else:
                # All in inches/feet
                radius_in = radius  # already in inches
                depth_ft = footing_depth  # already in feet
                # Volume in cubic feet: π * (r in feet)^2 * h in feet
                radius_ft = radius_in / 12
                volume_per_footing = math.pi * (radius_ft ** 2) * depth_ft  # cubic feet per footing
                total_concrete = volume_per_footing * num_footings  # cubic feet total
                bag_coverage = {40: 0.3, 60: 0.45, 80: 0.6}.get(bag_size, 0.3)  # cubic feet per bag

            num_bags = math.ceil(total_concrete / bag_coverage)

            # Set results
            results = {
                'num_footings': num_footings,
                'total_concrete': total_concrete,
                'total_concrete_unit': 'm³' if user_prefers_metric else 'cu ft',
                'num_bags': num_bags,
                'deck_area': deck_area,
                'beam_length': beam_length,
                'post_spacing': post_spacing,
                'num_beams': num_beams,
                'footing_diameter': footing_diameter,
                'footing_depth': footing_depth,
                'concrete_bag_size': bag_size,
            }
        except Exception as e:
            results = {'error': 'Invalid input. Please check your values.'}

    context = {
        'active_tab': 'footings',
        'results': results,
        'user_prefers_metric': user_prefers_metric,
    }
    return render(request, 'decking/footings.html', context)

