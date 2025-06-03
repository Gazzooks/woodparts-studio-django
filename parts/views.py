from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q, Sum
from .models import Part, PartTemplate
from .forms import PartForm, PartTemplateForm, BulkPartForm
from projects.models import Project

class PartsManagerView(LoginRequiredMixin, ListView):
    """Parts manager - equivalent to your PartsManager tool"""
    model = Part
    template_name = 'parts/parts_manager.html'
    context_object_name = 'parts'
    paginate_by = 50
    
    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        queryset = Part.objects.filter(project__owner=self.request.user)
        
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        
        # Add filtering and searching
        search = self.request.GET.get('search')
        material = self.request.GET.get('material')
        category = self.request.GET.get('category')
        
        if search:
            queryset = queryset.filter(
                Q(partname__icontains=search) |
                Q(material__icontains=search) |
                Q(notes__icontains=search)
            )
        
        if material:
            queryset = queryset.filter(material=material)
            
        if category:
            queryset = queryset.filter(category=category)
        
        return queryset.order_by('partname')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs.get('project_id')
        
        if project_id:
            context['project'] = get_object_or_404(
                Project, 
                id=project_id, 
                owner=self.request.user
            )
        
        # Add filter options
        all_parts = Part.objects.filter(project__owner=self.request.user)
        context['available_materials'] = all_parts.values_list('material', flat=True).distinct()
        context['available_categories'] = all_parts.values_list('category', flat=True).distinct()
        
        # Add summary statistics
        queryset = self.get_queryset()
        context['total_parts'] = queryset.count()
        context['total_quantity'] = sum(part.quantity for part in queryset)
        context['total_board_feet'] = sum(part.board_feet for part in queryset)
        
        return context

class PartCreateView(LoginRequiredMixin, CreateView):
    """Create new part"""
    model = Part
    form_class = PartForm
    template_name = 'parts/part_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, f"Part '{form.instance.partname}' created successfully!")
        return super().form_valid(form)
    
    def get_success_url(self):
        if self.object.project:
            return f"/parts/manager/{self.object.project.id}/"
        return "/parts/manager/"

class PartUpdateView(LoginRequiredMixin, UpdateView):
    """Update existing part"""
    model = Part
    form_class = PartForm
    template_name = 'parts/part_form.html'
    
    def get_queryset(self):
        return Part.objects.filter(project__owner=self.request.user)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, f"Part '{form.instance.partname}' updated successfully!")
        return super().form_valid(form)

class PartDeleteView(LoginRequiredMixin, DeleteView):
    """Delete part with confirmation"""
    model = Part
    template_name = 'parts/part_confirm_delete.html'
    
    def get_queryset(self):
        return Part.objects.filter(project__owner=self.request.user)
    
    def get_success_url(self):
        if self.object.project:
            return f"/parts/manager/{self.object.project.id}/"
        return "/parts/manager/"
    
    def delete(self, request, *args, **kwargs):
        part = self.get_object()
        part_name = part.partname
        result = super().delete(request, *args, **kwargs)
        messages.success(request, f"Part '{part_name}' deleted successfully!")
        return result

@login_required
def add_part_ajax(request):
    """AJAX endpoint for adding parts - equivalent to your add_part method"""
    if request.method == 'POST':
        form = PartForm(request.POST, user=request.user)
        if form.is_valid():
            part = form.save()
            return JsonResponse({
                'success': True,
                'part_id': part.id,
                'part_name': part.partname,
                'message': f"Part '{part.partname}' added successfully",
                'board_feet': part.board_feet,
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def bulk_edit_parts(request, project_id):
    """Bulk edit parts for a project"""
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    
    if request.method == 'POST':
        form = BulkPartForm(request.POST)
        if form.is_valid():
            part_ids = request.POST.getlist('selected_parts')
            parts = Part.objects.filter(id__in=part_ids, project=project)
            
            # Apply bulk changes
            changes = {}
            if form.cleaned_data.get('material'):
                changes['material'] = form.cleaned_data['material']
            if form.cleaned_data.get('category'):
                changes['category'] = form.cleaned_data['category']
            
            if changes:
                parts.update(**changes)
                messages.success(request, f"Updated {parts.count()} parts successfully!")
            
            return redirect('parts:manager', project_id=project.id)
    else:
        form = BulkPartForm()
    
    parts = project.parts.all()
    return render(request, 'parts/bulk_edit.html', {
        'form': form,
        'project': project,
        'parts': parts
    })

@login_required
def part_templates_list(request):
    """List part templates"""
    templates = PartTemplate.objects.filter(created_by=request.user).order_by('category', 'name')
    return render(request, 'parts/templates_list.html', {'templates': templates})

@login_required
def create_part_from_template(request, template_id, project_id):
    """Create a part from a template"""
    template = get_object_or_404(PartTemplate, id=template_id, created_by=request.user)
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    
    part = Part.objects.create(
        project=project,
        partname=template.name,
        length=template.length,
        width=template.width,
        thickness=template.thickness,
        material=template.material,
        category=template.category,
        quantity=1
    )
    
    messages.success(request, f"Part '{part.partname}' created from template!")
    return redirect('parts:manager', project_id=project.id)