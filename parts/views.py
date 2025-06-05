# parts/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Part
from .forms import PartForm
from accounts.models import UserPreferences

class PartListView(LoginRequiredMixin, ListView):
    model = Part
    template_name = 'parts/part_list.html'
    context_object_name = 'parts'
    paginate_by = 10

    def get_queryset(self):
        # Optional: Filter parts by the current user's projects if needed
        # Example: return Part.objects.filter(project__owner=self.request.user)
        return super().get_queryset()

class PartCreateView(LoginRequiredMixin, CreateView):
    model = Part
    form_class = PartForm
    template_name = 'parts/part_form.html'
    success_url = reverse_lazy('parts:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class PartUpdateView(LoginRequiredMixin, UpdateView):
    model = Part
    form_class = PartForm
    template_name = 'parts/part_form.html'
    success_url = reverse_lazy('parts:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class PartDeleteView(LoginRequiredMixin, DeleteView):
    model = Part
    template_name = 'parts/part_confirm_delete.html'
    success_url = reverse_lazy('parts:list')
