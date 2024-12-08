import json
import logging
from re import L
import requests
import os

from django.http import JsonResponse
from .models import Notification
from .addLog import Log

service_name = "notification_service"

logger = logging.getLogger(__name__)

def notification_type_request(request):
    if request.method == "POST":
        data = json.loads(request.body)
        logger.fatal(f"Creating notification: {data}")
        Log.add_log(service_name, (f"Creating notification: {data}"), request)
        
        
        receiver_username = data.get("receiver_username")
        sender_username = data.get("sender_username")
        type = data.get("type")
        content = data.get("content")

        notification = create_notification(receiver_username, type, content, sender_username)

        Log.add_log(service_name, (f"Notification created: {notification}"), request)
        return JsonResponse({"data": {"message": "Notification created"}}, status=201)

def create_notification(receiver_username, type, content, sender_username):
    notification = Notification.objects.create(
        receiver_username=receiver_username, type=type, content=content, sender_username=sender_username
    )
    logger.fatal(f"Notification created: {notification}")
    Log.add_log(service_name, (f"Notification created: {notification}"), None)
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
        logger.fatal(f"Getting notifications for user: {username}")

        notifications = (
            Notification.objects.filter(receiver_username=username, is_read=False)
            .order_by("-id")[:50]
            .values()
        )

        Log.add_log(service_name, (f"Notifications for user: {username}"), request)
        return JsonResponse({"data": list(notifications)}, status=200)

def notification_read(request, notification_id):
    if request.method == "PATCH":
        access_token = request.headers.get("Authorization")

        auth_service_url = os.environ.get("AUTH_SERVICE_URL")
        access_user = requests.get(
            f"{auth_service_url}/auth/access-token-by-username/",
            headers={"Authorization": access_token},
        )

        username = access_user.json().get("data").get("username")

        notification = Notification.objects.get(id=notification_id)
        if notification.receiver_username != username:
            Log.add_log(service_name, (f"User {username} is not authorized to read notification {notification_id}"), request)
            return JsonResponse(
                {"data": {"message": "You are not authorized to read this notification"}},
                status=403,
            )

        notification.is_read = True
        notification.save()

        Log.add_log(service_name, (f"Notification read: {notification_id}"), request)
        return JsonResponse({"data": {"message": "Notification read"}}, status=200)