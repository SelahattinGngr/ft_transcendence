import json
import logging
import requests
import os

from django.http import JsonResponse
from .models import Notification
from .ResponseService import ResponseService
from .Messages import Messages


logger = logging.getLogger(__name__)

def deneme(request):
    logger.fatal('This is a fatal log message')
    return JsonResponse({'message': 'Hello, World!'})

def notification_type_request(request):
    language = request.headers.get("Accept-Language", "en")

    if request.method == "POST":
        data = json.loads(request.body)
        user_name = data.get("user_name")
        type = data.get("type")
        #content = data.get("content")
        #title = data.get("type")
        is_read = False

        if not user_name:
            return ResponseService.create_error_response(
                Messages.USER_NOT_FOUND, language, 400, type
            )
            


