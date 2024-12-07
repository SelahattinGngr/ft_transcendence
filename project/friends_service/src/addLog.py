import logging
import os

import requests
logger = logging.getLogger(__name__)

class Log:
    def add_log(service_name, log_message, request):
        log_service_url = os.environ.get("LOG_SERVICE_URL")
        log_api_url = f"{log_service_url}/log/add-log/"
        log_data = {
            "service_name": service_name,
            "log_message": log_message,
            "ip_address": Log.get_client_ip(request),
        }
        requests.post(log_api_url, json=log_data)

    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip