# views.py
import json
import logging
import os

from django.http import JsonResponse
import requests

from .kafka_producer import send_message
from .Messages import Messages
from .models import friend_requests
from .ResponseService import ResponseService

logger = logging.getLogger(__name__)


# arkadaslık isteği gönderme
def send_friend_request(request):
    language = request.headers.get("Accept-Language", "tr")

    if request.method == "POST":
        access_token = request.headers.get("Authorization")
        if access_token is None:
            return ResponseService.create_error_response(
                Messages.NO_ACCESS_TOKEN, language, 401
            )

        logger.fatal(f"access token -> {access_token}")
        auth_service_url = os.environ.get("AUTH_SERVICE_URL")
        access_user = requests.get(
            f"{auth_service_url}/auth/access-token-by-username/",
            headers={"Authorization": access_token},
        )

        if access_user.status_code != 200:
            return ResponseService.create_error_response(
                Messages.INVALID_ACCESS_TOKEN, language, 401
            )

        data = json.loads(request.body)
        username = access_user.json().get("data").get("username")
        friend_username = data.get("friend_username")

        if not friend_username:
            return ResponseService.create_error_response(
                Messages.REQUIRED_FIELDS, language, 400
            )

        if username == friend_username:
            return ResponseService.create_error_response(
                Messages.CANNOT_ADD_SELF, language, 400
            )

        user_service_url = os.environ.get("USER_SERVICE_URL")
        friend_user = requests.get(f"{user_service_url}/user/{friend_username}/")

        if friend_user.status_code != 200:
            return JsonResponse(friend_user.json(), status=friend_user.status_code)

        # İsteğin zaten mevcut olup olmadığını kontrol eder
        ex_request = friend_requests.objects.filter(
            sender_username=username, receiver_username=friend_username
        ).first()

        if ex_request:
            if ex_request.status == "pending":
                return ResponseService.create_error_response(
                    Messages.REQUEST_ALREADY_SENT, language, 400
                )

        # İstek mevcut değilse yeni bir arkadaşlık isteği oluşturun
        friend_requests_obj = friend_requests.objects.create(
            sender_username=username,
            receiver_username=friend_username,
            status="pending",
        )

        # Kafka ile bildirim mesajı gönder
        notification_message = {
            "receiver_username": friend_username,
            "friend_request_id": friend_requests_obj.id,
            "message": f"{username} wants to be your friend.",
        }

        try:
            send_message(
                "user-notification-events",
                {
                    "type": "friend_request",
                    "content": notification_message,
                    "username": friend_username,
                },
            )
        except Exception as e:
            logger.error(f"Kafka producer error: {e}")

        return ResponseService.create_success_response(
            {"message": Messages.get_message(Messages.REQUEST_SENT_SUCCESS, language)},
            201,
        )

    return ResponseService.create_error_response(Messages.INVALID_METHOD, language, 405)


# arkadaslık isteğini reddetme
def reject_to_friend_request(request, id):
    language = request.headers.get("Accept-Language", "tr")

    if request.method == "GET":
        # access token ile kontrol eklenecek
        friend_request = friend_requests.objects.filter(id=id).first()
        if not friend_request:
            return ResponseService.create_error_response(
                Messages.REQUEST_NOT_FOUND, language, 404
            )
        friend_request.delete()

        return ResponseService.create_success_response(
            Messages.get_message(Messages.REQUEST_REJECTED, language), 200
        )

    return ResponseService.create_error_response(Messages.INVALID_METHOD, language, 405)


# arkadaslık isteğini kabul etme
def accept_friend_request(request, id):
    language = request.headers.get("Accept-Language", "tr")

    if request.method == "GET":
        # access token ile kontrol eklenecek
        friend_request = friend_requests.objects.filter(id=id).first()
        if not friend_request:
            return ResponseService.create_error_response(
                Messages.REQUEST_NOT_FOUND, language, 404
            )
        if friend_request.status != "pending":
            return ResponseService.create_error_response(
                Messages.REQUEST_ALREADY_ANSWERED, language, 400
            )

        friend_request.status = "accepted"
        friend_request.save()

        # send notification
        # notification_service_url = os.environ.get('NOTIFICATION_SERVICE_URL')
        # requests.post(f'{notification_service_url}/notifications/send/', json={
        #     'receiver_username': friend_request.sender_username,
        #     'message': f'{friend_request.receiver_username} accepted your friend request.'
        # })

        # bu kısım kafka ile yeniden yazılacak
        user_service_url = os.environ.get("USER_SERVICE_URL")
        requests.post(
            f"{user_service_url}/user/add_friend/",
            json={
                "username": friend_request.sender_username,
                "friend_username": friend_request.receiver_username,
            },
        )

        return ResponseService.create_success_response(
            Messages.get_message(Messages.REQUEST_ACCEPTED, language), 200
        )

    return ResponseService.create_error_response(Messages.INVALID_METHOD, language, 405)
