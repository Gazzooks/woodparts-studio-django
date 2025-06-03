from django.views.generic import ListView, CreateView, DetailView
from .models import StockMaterial

class MaterialListView(ListView):
    model = StockMaterial
    template_name = 'materials/list.html'
    context_object_name = 'materials'

class MaterialCreateView(CreateView):
    model = StockMaterial
    fields = ['material', 'length', 'width', 'thickness', 'quantity', 'price']
    template_name = 'materials/form.html'
    success_url = '/materials/'

class MaterialDetailView(DetailView):
    model = StockMaterial
    template_name = 'materials/detail.html'
    context_object_name = 'material'
