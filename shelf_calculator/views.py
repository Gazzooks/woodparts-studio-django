from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def shelf_calculator(request):
    if request.method == 'POST':
        try:
            interior_height = float(request.POST.get('interior_height', 0))
            shelf_thickness = float(request.POST.get('shelf_thickness', 0))
            num_shelves = int(request.POST.get('num_shelves', 1))
            spacing_option = request.POST.get('spacing_option', 'even')

            if num_shelves < 1:
                return JsonResponse({'success': False, 'error': 'Number of shelves must be at least 1.'})

            if spacing_option == 'even':
                if num_shelves < 2:
                    return JsonResponse({'success': False, 'error': 'Number of shelves must be at least 2 for even spacing.'})
                spacing = (interior_height - (num_shelves * shelf_thickness)) / (num_shelves - 1)
                result = f"Shelf spacing: {spacing:.2f} mm"
            else:
                # Collect custom shelf positions
                shelf_positions = []
                for i in range(1, num_shelves + 1):
                    pos = request.POST.get(f'shelf_pos_{i}')
                    if pos is not None:
                        shelf_positions.append(float(pos))
                if not shelf_positions:
                    return JsonResponse({'success': False, 'error': 'Please enter custom shelf positions.'})
                # Sort and validate positions (optional)
                shelf_positions.sort()
                if shelf_positions[-1] > interior_height:
                    return JsonResponse({'success': False, 'error': 'Shelf positions exceed cabinet height.'})
                result = f"Custom shelf positions (from bottom): " + ", ".join(f"{p:.2f} mm" for p in shelf_positions)

            return JsonResponse({'success': True, 'result': result})
        except Exception as e:
            return JsonResponse({'success': False, 'error': 'Invalid input. Please check your values.'})

    return render(request, 'shelf_calculator/shelf.html')
