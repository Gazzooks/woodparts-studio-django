from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Count, Sum, Q
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Project, ProjectTimeline, ProjectNote
from .forms import ProjectForm, ProjectSettingsForm, ProjectNoteForm
from parts.models import Part
import json


# Create a simple DashboardView first - we'll expand it later when models are ready
class DashboardView(LoginRequiredMixin, TemplateView):
    """Main dashboard view for logged-in users"""
    template_name = 'projects/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Recent projects: get the 5 most recent by date created
        context['recent_projects'] = Project.objects.order_by('-datecreated')[:5]
        # Optional: Add other dynamic stats as needed (total_projects, active_projects, etc.)
        context['total_projects'] = Project.objects.count()
        context['active_projects'] = Project.objects.filter(status='active')
        context['completed_projects'] = Project.objects.filter(status='completed')
        # Optional: Add total_parts if you have a related model
        # context['total_parts'] = Part.objects.count()  # Uncomment if you have a Part model
        return context

# Alias for backward compatibility
ProjectDashboardView = DashboardView

# Placeholder views - we'll implement these properly after models are working
class ProjectListView(LoginRequiredMixin, ListView):
    """List all projects for the current user"""
    model = Project
    template_name = 'projects/project_list.html'  # Optional, Django will look for this by default
    context_object_name = 'object_list'

# class ProjectDetailView(LoginRequiredMixin, TemplateView):
#     """Project detail view"""
#     template_name = 'projects/project_detail.html'
class ProjectDetailView(DetailView):
    model = Project
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_project'] = self.get_object()
        return context

class ProjectCreateView(LoginRequiredMixin, CreateView):
    """Create new project"""
    model = Project
    fields = ['name', 'description', 'status', 'notes', 'owner']
    # template_name = 'projects/project_form.html'  # (Optional: Django will look for this by default)
    success_url = reverse_lazy('projects:list')

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    """Update existing project"""
    model = Project
    fields = ['name', 'description', 'status', 'notes']  # Owner is now removed
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('projects:list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    """Delete project"""
    template_name = 'projects/project_confirm_delete.html'

    """Delete project with confirmation"""
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('projects:list')
    
    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        project = self.get_object()
        project_name = project.name
        result = super().delete(request, *args, **kwargs)
        messages.success(request, f"Project '{project_name}' deleted successfully!")
        return result

@login_required
def project_duplicate(request, pk):
    """Duplicate an existing project"""
    original_project = get_object_or_404(Project, pk=pk, owner=request.user)
    
    # Create new project
    new_project = Project.objects.create(
        name=f"{original_project.name} - Copy",
        description=original_project.description,
        status='planning',
        notes=original_project.notes,
        owner=request.user
    )
    
    # Copy all parts
    for part in original_project.parts.all():
        Part.objects.create(
            project=new_project,
            partname=part.partname,
            length=part.length,
            width=part.width,
            thickness=part.thickness,
            material=part.material,
            quantity=part.quantity,
            angle=part.angle,
            orientation=part.orientation,
            notes=part.notes,
            category=part.category,
            priority=part.priority
        )
    
    messages.success(request, f"Project duplicated as '{new_project.name}'")
    return redirect('projects:detail', pk=new_project.pk)

@login_required
def project_export(request, pk):
    """Export project data as JSON"""
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    
    # Prepare export data
    export_data = {
        'project': {
            'name': project.name,
            'description': project.description,
            'status': project.status,
            'notes': project.notes,
            'created': project.datecreated.isoformat(),
            'modified': project.datemodified.isoformat(),
        },
        'parts': []
    }
    
    for part in project.parts.all():
        export_data['parts'].append({
            'partname': part.partname,
            'length': float(part.length),
            'width': float(part.width),
            'thickness': float(part.thickness),
            'material': part.material,
            'quantity': part.quantity,
            'angle': float(part.angle) if part.angle else None,
            'orientation': part.orientation,
            'notes': part.notes,
            'category': part.category,
        })
    
    response = HttpResponse(
        json.dumps(export_data, indent=2),
        content_type='application/json'
    )
    response['Content-Disposition'] = f'attachment; filename="{project.name}_export.json"'
    return response

@login_required
def project_statistics_api(request, pk):
    """API endpoint for project statistics"""
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    parts = project.parts.all()
    
    stats = {
        'total_parts': parts.count(),
        'total_quantity': sum(part.quantity for part in parts),
        'total_board_feet': sum(part.board_feet for part in parts),
        'unique_materials': parts.values('material').distinct().count(),
        'completion_percentage': 0,
        'materials_breakdown': {}
    }
    
    if parts:
        completed_parts = parts.filter(is_completed=True).count()
        stats['completion_percentage'] = int((completed_parts / parts.count()) * 100)
    
    # Materials breakdown
    for part in parts:
        if part.material not in stats['materials_breakdown']:
            stats['materials_breakdown'][part.material] = {
                'count': 0,
                'board_feet': 0
            }
        stats['materials_breakdown'][part.material]['count'] += part.quantity
        stats['materials_breakdown'][part.material]['board_feet'] += part.board_feet
    
    return JsonResponse(stats)