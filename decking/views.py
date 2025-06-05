from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def deck_boards(request):
    # TODO: Add calculation logic here
    context = {
        'active_tab': 'deck_boards',
        # Add result variables as needed
    }
    return render(request, 'decking/deck_boards.html', context)

@login_required
def framing(request):
    # TODO: Add calculation logic here
    context = {
        'active_tab': 'framing',
        # Add result variables as needed
    }
    return render(request, 'decking/framing.html', context)

@login_required
def footings(request):
    # TODO: Add calculation logic here
    context = {
        'active_tab': 'footings',
        # Add result variables as needed
    }
    return render(request, 'decking/footings.html', context)
