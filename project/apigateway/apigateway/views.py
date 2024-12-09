import logging
import requests
from django.http import JsonResponse

from .addLog import Log

logger = logging.getLogger(__name__)

# TODO: auth işlemleri harici tüm servislere access token kontrolü eklenecek
# TODO: auth işlemlerinde bazı durumlar için access ve refresh token kontrolü yapılacak

# http://localhost:8000/auth/signup/
MICROSERVICES = {
    "auth": "http://authservice:8000",
    "user": "http://userservice:8000",
    "game": "http://gameservice:8000",
    "mail": "http://mailservice:8000",
    "tournament": "http://tournamentservice:8000",
    "matchmaking": "http://matchmakingservice:8000",
    "chat": "http://chatservice:8000",
    "friend": "http://friendservice:8000",
    "notification": "http://notificationservice:8000",
    "monitoring": "http://monitoringservice:8000",
    "log": "http://logservice:8000",
}

def proxy_request(request, path):   
    service_url = MICROSERVICES.get(path.split('/')[0], None)
    if not service_url:
        return JsonResponse({"error": "Invalid service name"}, status=400)
    
    log_message = f"incoming request: {request.method}"
    if request.body:
        log_message += f" {request.body}"
    Log.add_log(service_name=path, log_message=log_message, request=request)
    
    try:
        response = requests.request(
            method=request.method,
            url=f"{service_url}{request.path}",
            headers=request.headers,
            data=request.body
        )
    
        Log.add_log(service_name=path,
                    log_message=f"outgoing response: {response.status_code} {response.text}",
                    request=request)
        return JsonResponse(response.json(), status=response.status_code)
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": "Service request failed", "details": str(e)}, status=500)
