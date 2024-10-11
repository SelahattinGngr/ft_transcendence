import json
import logging

from django.http import JsonResponse

from .Messages import Messages
from .ResponseService import ResponseService
from .models import Avatar, Users

logger = logging.getLogger(__name__)


def intra_create(request):
    language = request.headers.get("Accept-Language", "en")
    if request.method != "POST":
        return ResponseService.create_error_response(
            Messages.INVALID_REQUEST_METHOD, language, 405
        )
    data = json.loads(request.body)

    username = data.get("username")
    email = data.get("email")

    if Users.objects.filter(username=username).exists():
        return ResponseService.create_error_response(
            Messages.USERNAME_ALREADY_EXISTS, language, 400
        )
    
    if Users.objects.filter(email=email).exists():
        return ResponseService.create_error_response(
            Messages.EMAIL_ALREADY_EXISTS, language, 400
        )
    
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    source_id = data.get("source_id")
    source = data.get("source")
    avatar_obj = data.get("avatar")

    avatar = Avatar.objects.create(
        url=avatar_obj.get("link"),
        large_url=avatar_obj.get("versions").get("large"),
        medium_url=avatar_obj.get("versions").get("medium"),
        small_url=avatar_obj.get("versions").get("small"),
        micro_url=avatar_obj.get("versions").get("micro"),
    )

    user = Users.objects.create(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        source_id=source_id,
        source=source,
        avatar_id=avatar,
    )

    logger.fatal(f"User created: {str(user)}")

    return JsonResponse(data, status=201)
