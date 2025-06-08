# parts/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Part
from .forms import PartForm
from accounts.models import UserPreferences
from django.shortcuts import get_object_or_404
from projects.models import Project
from django.http import JsonResponse
from django.template.loader import render_to_string

class PartListView(LoginRequiredMixin, ListView):
    model = Part
    template_name = 'parts/part_list.html'
    context_object_name = 'parts'
    paginate_by = 10

    def get_queryset(self):
        self.project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return Part.objects.filter(project=self.project)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        return context

class PartCreateView(LoginRequiredMixin, CreateView):
    model = Part
    form_class = PartForm
    template_name = 'parts/part_form.html'  # normal page view

    def get_project(self):
        return get_object_or_404(Project, pk=self.kwargs['project_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.get_project()
        return context

    def get_template_names(self):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['parts/part_form_modal.html']
        return [self.template_name]

    def form_valid(self, form):
        part = form.save(commit=False)
        part.project = self.get_project()
        part.save()
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            row_html = render_to_string('parts/part_row.html', {'part': part}, request=self.request)
            return JsonResponse({'success': True, 'row_html': row_html})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form_html = render_to_string(
                'parts/part_form_modal.html',
                {'form': form, 'project': self.get_project()},
                request=self.request
            )
            return JsonResponse({'success': False, 'form_html': form_html})
        return super().form_invalid(form)

class PartUpdateView(LoginRequiredMixin, UpdateView):
    model = Part
    form_class = PartForm
    template_name = 'parts/part_form_modal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.object.project
        return context

    def form_valid(self, form):
        part = form.save()
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            row_html = render_to_string('parts/part_row.html', {'part': part}, request=self.request)
            return JsonResponse({'success': True, 'row_html': row_html, 'part_id': part.id})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form_html = render_to_string(
                self.template_name,
                {'form': form, 'project': self.object.project},
                request=self.request
            )
            return JsonResponse({'success': False, 'form_html': form_html})
        return super().form_invalid(form)

class PartDeleteView(LoginRequiredMixin, DeleteView):
    model = Part

    def get_success_url(self):
        # self.object is available here and is the Part being deleted
        project_id = self.object.project.id
        return reverse_lazy('parts:list', kwargs={'project_id': project_id})
    