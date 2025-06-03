# project/context_processors.py
def current_project(request):
    project_id = request.resolver_match.kwargs.get('project_id') or request.session.get('current_project_id')
    if project_id:
        from projects.models import Project
        return {'current_project': Project.objects.get(id=project_id)}
    return {}
