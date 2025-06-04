# parts/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Part
from .forms import PartForm

class PartListView(ListView):
    model = Part
    template_name = 'parts/part_list.html'
    context_object_name = 'parts'
    paginate_by = 10

class PartCreateView(CreateView):
    model = Part
    form_class = PartForm
    template_name = 'parts/part_form.html'
    success_url = reverse_lazy('parts:list')

class PartUpdateView(UpdateView):
    model = Part
    form_class = PartForm
    template_name = 'parts/part_form.html'
    success_url = reverse_lazy('parts:list')

class PartDeleteView(DeleteView):
    model = Part
    template_name = 'parts/part_confirm_delete.html'
    success_url = reverse_lazy('parts:list')
