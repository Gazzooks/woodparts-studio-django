from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from .models import StockMaterial
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from materials.constants import IMPERIAL_LUMBER_SIZES, IMPERIAL_PLYWOOD_SIZES, METRIC_LUMBER_SIZES, METRIC_PLYWOOD_SIZES
from accounts.models import UserPreferences

class MaterialListView(LoginRequiredMixin,ListView):
    model = StockMaterial
    template_name = 'materials/list.html'
    context_object_name = 'materials'

    def get_queryset(self):
        # Optional: Filter by user's preferred unit system if needed
        user = self.request.user
        if hasattr(user, 'userpreferences'):
            unit_system = user.userpreferences.default_units
            return StockMaterial.objects.filter(unit_system=unit_system)
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_prefers_metric = False
        if hasattr(self.request.user, 'userpreferences'):
            user_prefers_metric = (self.request.user.userpreferences.default_units == 'metric')
        context['user_prefers_metric'] = user_prefers_metric
        return context

class MaterialCreateView(LoginRequiredMixin, CreateView):
    model = StockMaterial
    fields = ['material', 'thickness', 'width', 'length', 'quantity', 'price', 'notes', 'unit_system']
    template_name = 'materials/form.html'
    success_url = reverse_lazy('materials:list')

class MaterialDetailView(LoginRequiredMixin, DetailView):
    model = StockMaterial
    template_name = 'materials/detail.html'
    context_object_name = 'material'

class MaterialUpdateView(LoginRequiredMixin, UpdateView):
    model = StockMaterial
    fields = ['material', 'thickness', 'width', 'length', 'quantity', 'price', 'notes', 'unit_system']
    template_name = 'materials/form.html'
    success_url = reverse_lazy('materials:list')

class MaterialDeleteView(LoginRequiredMixin, DeleteView):
    model = StockMaterial
    template_name = 'materials/confirm_delete.html'
    success_url = reverse_lazy('materials:list')

class MaterialDuplicateView(LoginRequiredMixin, CreateView):
    model = StockMaterial
    template_name = 'materials/form.html'
    fields = ['material', 'thickness', 'width', 'length', 'quantity', 'price', 'notes', 'unit_system']
    success_url = reverse_lazy('materials:list')

    def get_initial(self):
        original = get_object_or_404(StockMaterial, pk=self.kwargs['pk'])
        return {
            'material': original.material,
            'thickness': original.thickness,
            'width': original.width,
            'length': original.length,
            'quantity': original.quantity,
            'price': original.price,
            'notes': original.notes,
            'unit_system': original.unit_system,
        }

def stock_list(request):
    # Get user preference (default to 'imperial' if not set, per your model)
    user_prefers_metric = False
    if hasattr(request.user, 'userpreferences'):
        user_prefers_metric = (request.user.userpreferences.default_units == 'metric')

    if user_prefers_metric:
        lumber_sizes = METRIC_LUMBER_SIZES
        plywood_sizes = METRIC_PLYWOOD_SIZES
    else:
        lumber_sizes = IMPERIAL_LUMBER_SIZES
        plywood_sizes = IMPERIAL_PLYWOOD_SIZES

    context = {
        'lumber_sizes': lumber_sizes,
        'plywood_sizes': plywood_sizes,
        'user_prefers_metric': user_prefers_metric,
    }
    return render(request, 'materials/stock_list.html', context)