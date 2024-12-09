import json
from .models import SavedLog
from django.http import JsonResponse
from django.core.paginator import Paginator

def save_log(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        service_name=data.get('service_name')
        log=data.get('log_message')
        log_ip=request.META.get('REMOTE_ADDR')
        SavedLog.objects.create(
            service_name=service_name,
            log=log,
            log_ip=log_ip
        )
        return JsonResponse({'message': 'Log saved successfully'}, status=201)
    return JsonResponse({'error': 'Invalid method'}, status=405)

def get_logs(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        page_number = data.get('page', 1)
        logs = SavedLog.objects.all()
        paginator = Paginator(logs, 50)
        page_obj = paginator.get_page(page_number)
        return JsonResponse({'logs': list(page_obj), 'page': page_number, 'num_pages': paginator.num_pages})
    return JsonResponse({'error': 'Invalid method'}, status=405)

def get_logs_by_service(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        service_name = data.get('service_name')
        page_number = data.get('page', 1)
        logs = SavedLog.objects.filter(service_name=service_name)
        paginator = Paginator(logs, 50)  # Show 10 logs per page
        page_obj = paginator.get_page(page_number)
        return JsonResponse({'logs': list(page_obj), 'page': page_number, 'num_pages': paginator.num_pages})
    return JsonResponse({'error': 'Invalid method'}, status=405)

def get_logs_by_ip(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        log_ip = data.get('log_ip')
        page_number = data.get('page', 1)
        logs = SavedLog.objects.filter(log_ip=log_ip)
        paginator = Paginator(logs, 50)  # Show 10 logs per page
        page_obj = paginator.get_page(page_number)
        return JsonResponse({'logs': list(page_obj), 'page': page_number, 'num_pages': paginator.num_pages})
    return JsonResponse({'error': 'Invalid method'}, status=405)
