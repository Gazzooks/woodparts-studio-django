from datetime import datetime
import csv
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Tool, ToolMaintenance
from .forms import ToolForm, ToolMaintenanceForm,ToolImportForm, MaintenanceImportForm  # You will need to create these forms
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string

def manager(request):
    """
    Main view for Shop Assets Manager.
    Displays Tools and Maintenance Log tabs with all records.
    """
    tools = Tool.objects.all().order_by('name')
    maintenance_records = ToolMaintenance.objects.select_related('tool').all().order_by('-maintenance_date')

    context = {
        'tools': tools,
        'maintenance_records': maintenance_records,
    }
    return render(request, 'shop_assets/manager.html', context)

# --- Tool CRUD views ---
def add_tool(request):
    if request.method == 'POST':
        form = ToolForm(request.POST)
        if form.is_valid():
            tool = form.save()
            # Render the new row for the table as HTML
            row_html = render_to_string('shop_assets/tool_row.html', {'tool': tool})
            return JsonResponse({'success': True, 'row_html': row_html})
        else:
            # Return form with errors as HTML
            form_html = render_to_string('shop_assets/tool_form.html', 
                                         {'form': form, 'action': 'Add Tool'}, request=request)
            return JsonResponse({'success': False, 'form_html': form_html})
    else:
        form = ToolForm()
        form_html = render_to_string('shop_assets/tool_form.html', 
                                     {'form': form, 'action': 'Add Tool'}, request=request)
        return JsonResponse({'success': False, 'form_html': form_html})
    
def edit_tool(request, pk):
    tool = get_object_or_404(Tool, pk=pk)
    if request.method == 'POST':
        form = ToolForm(request.POST, instance=tool)
        if form.is_valid():
            tool = form.save()
            row_html = render_to_string('shop_assets/tool_row.html', {'tool': tool})
            return JsonResponse({'success': True, 'row_html': row_html, 'tool_id': tool.id})
        else:
            form_html = render_to_string('shop_assets/tool_form.html', 
                                         {'form': form, 'action': 'Edit Tool'}, request=request)
            return JsonResponse({'success': False, 'form_html': form_html})
    else:
        form = ToolForm(instance=tool)
        form_html = render_to_string('shop_assets/tool_form.html',
                                      {'form': form, 'action': 'Edit Tool', 'tool': tool}, request=request)
    return JsonResponse({'success': False, 'form_html': form_html})

def delete_tool(request, pk):
    tool = get_object_or_404(Tool, pk=pk)
    if request.method == 'POST':
        tool.delete()
        return JsonResponse({'success': True, 'tool_id': pk})
    else:
        form_html = render_to_string('shop_assets/tool_confirm_delete.html', {'tool': tool}, request=request)
        return JsonResponse({'form_html': form_html})

# --- Maintenance CRUD views ---
def add_maintenance(request):
    initial = {}
    tool_id = request.GET.get('tool')
    if tool_id:
        initial['tool'] = tool_id
    if request.method == 'POST':
        form = ToolMaintenanceForm(request.POST)
        if form.is_valid():
            record = form.save()
            row_html = render_to_string('shop_assets/maintenance_row.html', {'record': record})
            return JsonResponse({'success': True, 'row_html': row_html})
        else:
            form_html = render_to_string('shop_assets/maintenance_form.html', {'form': form, 'action': 'Add Maintenance Record'}, request=request)
            return JsonResponse({'success': False, 'form_html': form_html})
    else:
        form = ToolMaintenanceForm(initial=initial)
        form_html = render_to_string('shop_assets/maintenance_form.html', {'form': form, 'action': 'Add Maintenance Record'}, request=request)
        return JsonResponse({'success': False, 'form_html': form_html})

def edit_maintenance(request, pk):
    record = get_object_or_404(ToolMaintenance, pk=pk)
    if request.method == 'POST':
        form = ToolMaintenanceForm(request.POST, instance=record)
        if form.is_valid():
            record = form.save()
            row_html = render_to_string('shop_assets/maintenance_row.html', {'record': record})
            return JsonResponse({'success': True, 'row_html': row_html, 'record_id': record.id})
        else:
            form_html = render_to_string('shop_assets/maintenance_form.html', {'form': form, 'action': 'Edit Maintenance Record', 'record': record}, request=request)
            return JsonResponse({'success': False, 'form_html': form_html})
    else:
        form = ToolMaintenanceForm(instance=record)
        form_html = render_to_string('shop_assets/maintenance_form.html', {'form': form, 'action': 'Edit Maintenance Record', 'record': record}, request=request)
        return JsonResponse({'success': False, 'form_html': form_html})

def delete_maintenance(request, pk):
    record = get_object_or_404(ToolMaintenance, pk=pk)
    if request.method == 'POST':
        record.delete()
        return JsonResponse({'success': True, 'record_id': pk})
    else:
        form_html = render_to_string('shop_assets/maintenance_confirm_delete.html', {'record': record}, request=request)
        return JsonResponse({'form_html': form_html})

# --- Tools - Export/Import View ---
def export_tools(request):
    today_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"tools_{today_str}.csv"

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Type', 'Serial Number', 'Brand', 'Model', 'Purchase Date', 'Purchase Price', 'Location', 'Notes'])
    for tool in Tool.objects.all():
        writer.writerow([
            tool.name,
            tool.type,
            tool.serial_number,
            tool.brand,
            tool.model,
            tool.purchase_date,
            tool.purchase_price,
            tool.location,
            tool.notes
        ])
    return response

def import_tools(request):
    if request.method == 'POST':
        form = ToolImportForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            count = 0
            for row in reader:
                Tool.objects.create(
                    name=row.get('Name', ''),
                    type=row.get('Type', ''),
                    serial_number=row.get('Serial Number', ''),
                    brand=row.get('Brand', ''),
                    model=row.get('Model', ''),
                    purchase_date=row.get('Purchase Date') or None,
                    purchase_price=row.get('Purchase Price') or None,
                    location=row.get('Location', ''),
                    notes=row.get('Notes', ''),
                )
                count += 1
            return JsonResponse({'success': True, 'count': count})
        else:
            form_html = render_to_string('shop_assets/import_form.html', {'form': form, 'action': 'Import Tools'}, request=request)
            return JsonResponse({'success': False, 'form_html': form_html})
    else:
        form = ToolImportForm()
        form_html = render_to_string('shop_assets/import_form.html', {'form': form, 'action': 'Import Tools'}, request=request)
        return JsonResponse({'success': False, 'form_html': form_html})

def import_maintenance(request):
    if request.method == 'POST':
        form = MaintenanceImportForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            count = 0
            for row in reader:
                tool_name = row.get('Tool', '')
                tool = Tool.objects.filter(name=tool_name).first()
                if tool:
                    ToolMaintenance.objects.create(
                        tool=tool,
                        maintenance_date=row.get('Date'),
                        maintenance_type=row.get('Type', ''),
                        notes=row.get('Notes', ''),
                    )
                    count += 1
            return JsonResponse({'success': True, 'count': count})
        else:
            form_html = render_to_string('shop_assets/import_form.html', {'form': form, 'action': 'Import Maintenance'}, request=request)
            return JsonResponse({'success': False, 'form_html': form_html})
    else:
        form = MaintenanceImportForm()
        form_html = render_to_string('shop_assets/import_form.html', {'form': form, 'action': 'Import Maintenance'}, request=request)
        return JsonResponse({'success': False, 'form_html': form_html})

def export_maintenance(request):
    today_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"maintenance_{today_str}.csv"

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    writer = csv.writer(response)
    writer.writerow(['Tool', 'Date', 'Type', 'Notes'])
    for record in ToolMaintenance.objects.select_related('tool').all():
        writer.writerow([
            record.tool.name if record.tool else '',
            record.maintenance_date,
            record.maintenance_type,
            record.notes
        ])
    return response
