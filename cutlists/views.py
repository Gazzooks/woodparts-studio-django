# cutlists/views.py

from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from projects.models import Project
from materials.models import StockMaterial
from .models import Cutlist, CutlistPart, CutlistStock
from .forms import CutlistForm, CutlistPartFormSet, CutlistStockFormSet

# Utility functions for unit conversion and kerf adjustment
def convert_units(value, units):
    # Placeholder: implement actual conversion logic
    # For now, assume value is in inches and convert to cm if units == 'metric'
    if units == 'metric':
        return round(value * 2.54, 2)
    return value

def adjust_for_kerf(length, kerf):
    # Adjust length by subtracting kerf thickness
    return round(length - kerf, 2) if length > kerf else 0

class CutlistCreateView(LoginRequiredMixin, CreateView):
    model = Cutlist
    form_class = CutlistForm
    template_name = 'cutlists/creator.html'  # Main interface

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(Project, id=self.kwargs['project_id'], owner=self.request.user)
        project_settings = getattr(project, 'settings', None)
        measurement_units = project_settings.measurement_units if project_settings else 'imperial'
        kerf_thickness = project_settings.default_thickness if project_settings else 0.0

        if self.request.POST:
            context['parts_formset'] = CutlistPartFormSet(self.request.POST, prefix='parts')
            context['stock_formset'] = CutlistStockFormSet(self.request.POST, prefix='stock')
        else:
            context['parts_formset'] = CutlistPartFormSet(prefix='parts')
            context['stock_formset'] = CutlistStockFormSet(prefix='stock')

        context['project'] = project
        context['measurement_units'] = measurement_units
        context['kerf_thickness'] = kerf_thickness

        # Check if project has parts
        if not project.parts.exists():
            context['no_parts'] = True

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        parts_formset = context['parts_formset']
        stock_formset = context['stock_formset']
        project = context['project']

        if not project.parts.exists():
            form.add_error(None, 'Cannot create a cutlist without parts in the project.')
            return self.form_invalid(form)

        with transaction.atomic():
            form.instance.project = project
            form.instance.created_by = self.request.user
            self.object = form.save()

            if parts_formset.is_valid():
                parts_formset.instance = self.object
                parts = parts_formset.save(commit=False)
                for part in parts:
                    part.cutlist = self.object
                    part.save()

            if stock_formset.is_valid():
                stock_formset.instance = self.object
                stock_items = stock_formset.save(commit=False)
                for stock in stock_items:
                    stock.cutlist = self.object
                    stock.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('projects:detail', kwargs={'pk': self.kwargs['project_id']})

class CutlistDetailView(LoginRequiredMixin, DetailView):
    model = Cutlist
    template_name = 'cutlists/creator.html'
    context_object_name = 'cutlist'

    def get_queryset(self):
        return Cutlist.objects.filter(project__owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cutlist = self.object
        project = cutlist.project
        project_settings = getattr(project, 'settings', None)
        measurement_units = project_settings.measurement_units if project_settings else 'imperial'
        kerf_thickness = project_settings.default_thickness if project_settings else 0.0

        # Prepare parts data with unit conversion and kerf adjustment
        parts_data = []
        for part in cutlist.cutlistpart_set.all():
            parts_data.append({
                'name': part.name,
                'length': convert_units(part.length, measurement_units),
                'width': convert_units(part.width, measurement_units),
                'thickness': convert_units(part.thickness, measurement_units),
                'quantity': part.quantity,
                'material': part.material,
                'notes': part.notes,
                'kerf_adjusted_length': adjust_for_kerf(part.length, kerf_thickness),
                'kerf_adjusted_width': adjust_for_kerf(part.width, kerf_thickness),
            })

        context['parts'] = parts_data
        context['measurement_units'] = measurement_units
        context['kerf_thickness'] = kerf_thickness
        context['project'] = project

        return context

class CutlistUpdateView(LoginRequiredMixin, UpdateView):
    model = Cutlist
    form_class = CutlistForm
    template_name = 'cutlists/creator.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object.project
        project_settings = getattr(project, 'settings', None)
        measurement_units = project_settings.measurement_units if project_settings else 'imperial'
        kerf_thickness = project_settings.default_thickness if project_settings else 0.0

        if self.request.POST:
            context['parts_formset'] = CutlistPartFormSet(
                self.request.POST, instance=self.object, prefix='parts'
            )
            context['stock_formset'] = CutlistStockFormSet(
                self.request.POST, instance=self.object, prefix='stock'
            )
        else:
            context['parts_formset'] = CutlistPartFormSet(
                instance=self.object, prefix='parts'
            )
            context['stock_formset'] = CutlistStockFormSet(
                instance=self.object, prefix='stock'
            )

        context['measurement_units'] = measurement_units
        context['kerf_thickness'] = kerf_thickness
        context['project'] = project

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        parts_formset = context['parts_formset']
        stock_formset = context['stock_formset']

        with transaction.atomic():
            self.object = form.save()

            if parts_formset.is_valid():
                parts_formset.save()

            if stock_formset.is_valid():
                stock_formset.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('cutlists:detail', kwargs={'pk': self.object.id})

# Entry point for menu access
def cutlist_creator_view(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    if not project.parts.exists():
        return render(request, 'cutlists/no_parts.html', {'project': project})
    cutlist = Cutlist.objects.filter(project=project).first()
    if cutlist:
        return redirect('cutlists:detail', pk=cutlist.id)
    else:
        return redirect('cutlists:create', project_id=project.id)
