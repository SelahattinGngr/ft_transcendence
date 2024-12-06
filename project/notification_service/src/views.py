import logging
import requests
import os

from django.http import JsonResponse
from .models import Notification


logger = logging.getLogger(__name__)

def notification_type_request(user_name, type, content):
    notification = Notification.objects.create(
        user_name=user_name, type=type, content=content
    )
    logger.fatal(f"Notification created: {notification}")
    return notification

def get_user_notifications(request):
    if request.method == "GET":
        access_token = request.headers.get("Authorization")

        auth_service_url = os.environ.get("AUTH_SERVICE_URL")
        access_user = requests.get(
            f"{auth_service_url}/auth/access-token-by-username/",
            headers={"Authorization": access_token},
        )

        username = access_user.json().get("data").get("username")

        notifications = (
            Notification.objects.filter(user_name=username, is_read=False)
            .order_by("-id")[:50]
            .values()
        )

        return JsonResponse({"data": list(notifications)}, status=200)
