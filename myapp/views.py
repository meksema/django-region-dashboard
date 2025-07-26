from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django_celery_results.models import TaskResult
from .forms import UploadFileForm
from .models import Applicant

from datetime import datetime
from django.core.paginator import Paginator
from .tasks import process_uploaded_file
@login_required(login_url='login')
def upload_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            file_path = default_storage.save(f'temp/{uploaded_file.name}', uploaded_file)
            full_path = default_storage.path(file_path)

            process_uploaded_file.delay(full_path)
            messages.success(request, "Upload received! Data is being processed in the background.")
            return redirect('dashboard')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

@login_required(login_url='login')
def dashboard(request):
    user_region = request.user.userprofile.region
    full_qs = Applicant.objects.filter(region=user_region)

    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if date_from:
        try:
            d0 = datetime.strptime(date_from, '%Y-%m-%d').date()
            full_qs = full_qs.filter(application_submitted_at__date__gte=d0)
        except ValueError:
            pass

    if date_to:
        try:
            d1 = datetime.strptime(date_to, '%Y-%m-%d').date()
            full_qs = full_qs.filter(application_submitted_at__date__lte=d1)
        except ValueError:
            pass

    # Pagination
    paginator = Paginator(full_qs, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_qs = page_obj.object_list
    start_index = page_obj.start_index()

    # Chart data
    gender_data = (
        full_qs.values('gender')
        .annotate(count=Count('id'))
        .order_by('gender')
    )
    genders = {e['gender'] or 'Unknown': e['count'] for e in gender_data}

    status_data = (
        full_qs.values('application_status')
        .annotate(count=Count('id'))
        .order_by('application_status')
    )
    statuses = {e['application_status'] or 'Unknown': e['count'] for e in status_data}

    title_data = (
        full_qs.values('nd_title')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    titles = {e['nd_title'] or 'Unknown': e['count'] for e in title_data}

    # Table data
    field_names = [f.name for f in Applicant._meta.fields if f.concrete and not f.auto_created]
    headers = [Applicant._meta.get_field(n).verbose_name.title() for n in field_names]
    rows_data = list(page_qs.values_list(*field_names))

    # Latest Celery task info
    latest_task = (
        TaskResult.objects
        .filter(task_name='myapp.tasks.process_uploaded_file')
        .order_by('-date_done')
        .first()
    )
    task_status = latest_task.status if latest_task else None
    task_time = latest_task.date_done if latest_task else None

    return render(request, 'dashboard.html', {
        'headers': headers,
        'rows_data': rows_data,
        'page_obj': page_obj,
        'start_index': start_index,
        'gender_chart': genders,
        'status_chart': statuses,
        'title_chart': titles,
        'filter_from': date_from or '',
        'filter_to': date_to or '',
        'task_status': task_status,
        'task_time': task_time,
    })
