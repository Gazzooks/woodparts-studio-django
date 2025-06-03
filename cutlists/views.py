# cutlists/views.py
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.db import transaction
from django.shortcuts import get_object_or_404
from projects.models import Project
from materials.models import StockMaterial
from .models import Cutlist, CutlistPart, CutlistStock
from .forms import CutlistForm, CutlistPartFormSet, CutlistStockFormSet

class CutlistCreateView(LoginRequiredMixin, CreateView):
    model = Cutlist
    form_class = CutlistForm
    template_name = 'cutlists/cutlist_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        
        if self.request.POST:
            context['parts_formset'] = CutlistPartFormSet(self.request.POST, prefix='parts')
            context['stock_formset'] = CutlistStockFormSet(self.request.POST, prefix='stock')
        else:
            context['parts_formset'] = CutlistPartFormSet(prefix='parts')
            context['stock_formset'] = CutlistStockFormSet(prefix='stock')
        
        context['project'] = project
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        parts_formset = context['parts_formset']
        stock_formset = context['stock_formset']
        project = context['project']

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
    template_name = 'cutlists/cutlist_detail.html'
    context_object_name = 'cutlist'

    def get_queryset(self):
        return Cutlist.objects.filter(project__owner=self.request.user)

class CutlistUpdateView(LoginRequiredMixin, UpdateView):
    model = Cutlist
    form_class = CutlistForm
    template_name = 'cutlists/cutlist_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
