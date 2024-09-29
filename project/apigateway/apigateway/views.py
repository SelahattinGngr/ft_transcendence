import logging
import requests
from django.http import JsonResponse

logger = logging.getLogger(__name__)

# Mikroservislerin URL'lerini burada bir dictionary olarak tanımla
MICROSERVICES = {
    "auth": "http://authservice:8000",
    "user": "http://user_service:10001",
    "game": "http://game_service:10002",
    "mail": "http://mail_service:10003",
    "tournament": "http://tournament_service:10004",
    "matchmaking": "http://matchmaking_service:10005",
    "chat": "http://chat_service:10006",
    "friend": "http://friend_service:10007",
    "notification": "http://notification_service:10008",
    "monitoring": "http://monitoring_service:10009"
}

def proxy_request(request, path):
    logger.info("Service Name: %s", path)  # Logger'ı kullan
    print("------------------------------------")
    print("Service Name:", path)
    print("------------------------------------")
    print(path.split('/')[0])
    print("------------------------------------")
    
    service_url = MICROSERVICES.get(path.split('/')[0], None)
    if not service_url:
        return JsonResponse({"error": "Invalid service name"}, status=400)

    try:
        print("------------------------------------")
        print(f"Proxying request to {path}")
        print("------------------------------------")
        response = requests.request(
            method=request.method,
            url=f"{service_url}{request.path}",
            headers=request.headers,
            data=request.body
        )
        return JsonResponse(response.json(), status=response.status_code)
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": "Service request failed", "details": str(e)}, status=500)
