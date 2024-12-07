from urllib import request
from .models import Saved_log

class logrequest:
    def __init__(self, service_name, log):
        self.service_name = service_name
        self.log = log

def save_log(logrequest):
    if request.method == 'POST':

        Saved_log.objects.create(
            service_name=logrequest.service_name,
            log=logrequest.log
        )

def get_logs():
    logs = Saved_log.objects.all()
    return logs

def get_logs_by_service(service_name):
    logs = Saved_log.objects.filter(service_name=service_name)
    return logs

