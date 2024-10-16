import json
import logging

from django.http import JsonResponse

from .Messages import Messages
from .models import Avatar, Users
from .ResponseService import ResponseService

logger = logging.getLogger(__name__)

def get_user(request, username):
    language = request.headers.get("Accept-Language", "en")
    if request.method != "GET":
        return ResponseService.create_error_response(
            Messages.INVALID_REQUEST_METHOD, language, 405
        )
    users = Users.objects.filter(username=username).first()
    if users is None:
        return ResponseService.create_error_response(
            Messages.USER_NOT_FOUND, language, 404
        )
    user = {
        "id": users.id,
        "username": users.username,
        "email": users.email,
        "first_name": users.first_name,
        "last_name": users.last_name,
        "bio": users.bio,
        "medium_avatar": users.avatar_id.medium_url,
        "small_avatar": users.avatar_id.small_url,
        "micro_avatar": users.avatar_id.micro_url,
    }
    return ResponseService.create_success_response(user, 200)


def create_user(request):
    language = request.headers.get("Accept-Language", "en")
    if request.method != "POST":
        return ResponseService.create_error_response(
            Messages.INVALID_REQUEST_METHOD, language, 405
        )

    try:
        data = json.loads(request.body.decode("utf-8"))
        avatar_url = data.get("avatar_url", "https://hizliresim.com/d0crqf0")
        logger.fatal(f"avatar_url: {data}")
        avatar = Avatar.objects.create(url=avatar_url)
        user = Users.objects.create(
            username=data["username"],
            email=data["email"],
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            source="auth_service",
            source_id=str(data.get("id")),
            status=True,
            avatar_id=avatar,
        )
        return ResponseService.create_success_response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            201,
        )

    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        return ResponseService.create_error_response(
            Messages.USER_CREATION_FAILED, language, 500
        )


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

    users = Users.objects.create(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        source_id=source_id,
        source=source,
        avatar_id=avatar,
    )

    user = {
        "id": users.id,
        "username": users.username,
        "email": users.email,
        "first_name": users.first_name,
        "last_name": users.last_name,
        "medium_avatar": users.avatar_id.medium_url,
        "small_avatar": users.avatar_id.small_url,
        "micro_avatar": users.avatar_id.micro_url,
    }
    return ResponseService.create_success_response(user, 201)

def update_profile(request, username):
    language = request.headers.get("Accept-Language", "en")
    if request.method != "PUT":
        return ResponseService.create_error_response(
            Messages.INVALID_REQUEST_METHOD, language, 405
        )

    try:
        user = Users.objects.filter(username=username).first()
        if not user:
            return ResponseService.create_error_response(
                Messages.USER_NOT_FOUND, language, 404
            )

        data = json.loads(request.body.decode("utf-8"))

        bio = data.get("bio", user.bio)
        avatar_url = data.get("avatar_url", user.avatar_id.url)

        if len(bio) > 255:
            return ResponseService.create_error_response(
                Messages.INVALID_BIO_LENGTH, language, 400
            )

        avatar = Avatar.objects.filter(id=user.avatar_id.id).first()
        if avatar:
            avatar.url = avatar_url
            avatar.save()

        user.bio = bio
        user.save()

        updated_user = {
            "id": user.id,
            "username": user.username,
            "bio": user.bio,
            "avatar_url": avatar.url,
        }

        return ResponseService.create_success_response(updated_user, 200)

    except Exception as e:
        logger.error(f"Error updating profile: {str(e)}")
        return ResponseService.create_error_response(
            Messages.PROFILE_UPDATE_FAILED, language, 500
        )
