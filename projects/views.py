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
        context.update({
            'user': self.request.user,
            'message': 'Welcome to WoodParts Studio!'
        })
        return context

# Alias for backward compatibility
ProjectDashboardView = DashboardView

# Placeholder views - we'll implement these properly after models are working
class ProjectListView(LoginRequiredMixin, TemplateView):
    """List all projects for the current user"""
    template_name = 'projects/project_list.html'

# class ProjectDetailView(LoginRequiredMixin, TemplateView):
#     """Project detail view"""
#     template_name = 'projects/project_detail.html'
class ProjectDetailView(DetailView):
    model = Project
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_project'] = self.get_object()
        return context

class ProjectCreateView(LoginRequiredMixin, TemplateView):
    """Create new project"""
    template_name = 'projects/project_form.html'

class ProjectUpdateView(LoginRequiredMixin, TemplateView):
    """Update existing project"""
    template_name = 'projects/project_form.html'

class ProjectDeleteView(LoginRequiredMixin, TemplateView):
    """Delete project"""
    template_name = 'projects/project_confirm_delete.html'

# class ProjectDashboardView(LoginRequiredMixin, TemplateView):
#     """Main project dashboard - equivalent to your welcome screen"""
#     template_name = 'projects/dashboard.html'
#     # context_object_name = 'recent_projects'
    
#     def get_queryset(self):
#         return Project.objects.filter(owner=self.request.user).order_by('-datemodified')[:10]
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user_projects = Project.objects.filter(owner=self.request.user)
        
#         context.update({
#             'total_projects': user_projects.count(),
#             'active_projects': user_projects.filter(status='active'),
#             'completed_projects': user_projects.filter(status='completed'),
#             'total_parts': Part.objects.filter(project__owner=self.request.user).count(),
#             'recent_activity': self.get_recent_activity(),
#         })
#         return context
    
#     def get_recent_activity(self):
#         """Get recent project activity"""
#         recent_projects = Project.objects.filter(
#             owner=self.request.user
#         ).order_by('-datemodified')[:5]
        
#         recent_parts = Part.objects.filter(
#             project__owner=self.request.user
#         ).order_by('-created_at')[:5]
        
#         return {
#             'projects': recent_projects,
#             'parts': recent_parts,
#         }

# class ProjectListView(LoginRequiredMixin, ListView):
#     """List all projects for the current user"""
#     model = Project
#     template_name = 'projects/project_list.html'
#     context_object_name = 'projects'
#     paginate_by = 20
    
#     def get_queryset(self):
#         queryset = Project.objects.filter(owner=self.request.user)
        
#         # Add filtering
#         status = self.request.GET.get('status')
#         search = self.request.GET.get('search')
        
#         if status:
#             queryset = queryset.filter(status=status)
        
#         if search:
#             queryset = queryset.filter(
#                 Q(name__icontains=search) | 
#                 Q(description__icontains=search)
#             )
        
#         return queryset.order_by('-datemodified')
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['status_choices'] = Project.STATUS_CHOICES
#         context['current_status'] = self.request.GET.get('status', '')
#         context['current_search'] = self.request.GET.get('search', '')
#         return context

# class ProjectDetailView(LoginRequiredMixin, DetailView):
#     """Project detail view - equivalent to your show_project_overview"""
#     model = Project
#     template_name = 'projects/project_detail.html'
#     context_object_name = 'project'
    
#     def get_queryset(self):
#         return Project.objects.filter(owner=self.request.user)
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         project = self.object
        
#         # Add statistics (equivalent to your project statistics)
#         parts = project.parts.all()
#         context.update({
#             'total_parts': parts.count(),
#             'total_quantity': sum(part.quantity for part in parts),
#             'unique_materials': parts.values('material').distinct().count(),
#             'total_board_feet': sum(part.board_feet for part in parts),
#             'recent_parts': parts.order_by('-created_at')[:5],
#             'project_timeline': project.timeline.all()[:5],
#             'recent_notes': project.project_notes.all()[:3],
#             'parts_by_material': self.get_parts_by_material(parts),
#             'completion_percentage': self.get_completion_percentage(parts),
#         })
        
#         return context
    
#     def get_parts_by_material(self, parts):
#         """Group parts by material"""
#         materials = {}
#         for part in parts:
#             if part.material not in materials:
#                 materials[part.material] = {
#                     'count': 0,
#                     'total_quantity': 0,
#                     'board_feet': 0
#                 }
#             materials[part.material]['count'] += 1
#             materials[part.material]['total_quantity'] += part.quantity
#             materials[part.material]['board_feet'] += part.board_feet
#         return materials
    
#     def get_completion_percentage(self, parts):
#         """Calculate project completion percentage"""
#         if not parts:
#             return 0
#         completed_parts = parts.filter(is_completed=True).count()
#         return int((completed_parts / parts.count()) * 100)

# class ProjectCreateView(LoginRequiredMixin, CreateView):
#     """Create new project - equivalent to your new_project method"""
#     model = Project
#     form_class = ProjectForm
#     template_name = 'projects/project_form.html'
    
#     def form_valid(self, form):
#         form.instance.owner = self.request.user
#         messages.success(self.request, f"Project '{form.instance.name}' created successfully!")
#         return super().form_valid(form)

# class ProjectUpdateView(LoginRequiredMixin, UpdateView):
#     """Update existing project"""
#     model = Project
#     form_class = ProjectForm
#     template_name = 'projects/project_form.html'
    
#     def get_queryset(self):
#         return Project.objects.filter(owner=self.request.user)
    
#     def form_valid(self, form):
#         messages.success(self.request, f"Project '{form.instance.name}' updated successfully!")
#         return super().form_valid(form)

# class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    """Delete project with confirmation"""
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = '/projects/'
    
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