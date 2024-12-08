from requests import request
from .models import Saved_log
from django.http import JsonResponse


class LogRequest:
    def __init__(self, service_name, log):
        self.service_name = service_name
        self.log = log

def save_log(logrequest):
    if request.method == 'POST':
        data = request.POST
        logrequest = LogRequest(
            service_name=data.get('service_name'),
            log=data.get('log')
        )
        Saved_log.objects.create(
            service_name=logrequest.service_name,
            log=logrequest.log
        )
        return JsonResponse({'message': 'Log saved successfully'}, status=201)
    return JsonResponse({'error': 'Invalid method'}, status=405)


def get_logs():
    logs = Saved_log.objects.all()
    return logs

def get_logs_by_service(service_name):
    logs = Saved_log.objects.filter(service_name=service_name)
    return logs

