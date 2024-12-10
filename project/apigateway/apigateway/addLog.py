import logging
import os

import requests
logger = logging.getLogger(__name__)

class Log:
    def add_log(service_name, log_message, request):
        try:
            log_service_url = os.environ.get("LOG_SERVICE_URL")
            if not log_service_url:
                logger.error("LOG_SERVICE_URL is not set.")
                return
            log_api_url = f"{log_service_url}/log/add-log/"
            headers = {
                "Content-Type": "application/json",
            }
            log_data = {
                "service_name": service_name,
                "log_message": log_message,
                "ip_address": Log.get_client_ip(request),
            }
            response = requests.post(log_api_url, json=log_data, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending log: {str(e)}")

    # TODO: gateway containerinin ip adresini alıyor, client ip alınmalı
    def get_client_ip(request):
        try:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                return x_forwarded_for.split(',')[0]
            return request.META.get('REMOTE_ADDR', 'unknown')
        except AttributeError:
            logger.error("Request object has no META attribute.")
            return "unknown"
