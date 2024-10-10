import json
import logging
import os
import uuid

from django.http import JsonResponse
import requests
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from .Messages import Messages
from .models import MailTokens, Users
from .ResponseService import ResponseService
from .TokenService import TokenService

logger = logging.getLogger(__name__)


def send_verification_email(user, token):
    # Mail servisine API isteği gönderme kısmı yorum satırı olarak bırakıldı
    # Bu kısım daha sonra gerçek mail servisine entegre edilecek
    # Example: Send POST request to the mail microservice
    # mail_service_url = "http://mailservice/send_verification"
    # response = requests.post(mail_service_url, json={"email": user.email, "token": token})
    # if response.status_code == 200:
    #     logger.info(f"Verification email sent to {user.email}")
    # else:
    #     logger.error(f"Failed to send email to {user.email}: {response.text}")

    # Şu an için dümenden mail gönderim
    logger.info(f"Verification email sent to {user.email} with token: {token}")
    print(f"[INFO] Verification email to: {user.email}, Token: {token}")


def signup(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        language = request.headers.get("Accept-Language", "en")
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if (
            len(password) < 8
            or not any(char.isdigit() for char in password)
            or not any(char.isalpha() for char in password)
        ):
            return ResponseService.create_error_response(
                Messages.WEAK_PASSWORD, language, 400
            )

        try:
            validate_email(email)
        except ValidationError:
            return ResponseService.create_error_response(
                Messages.INVALID_EMAIL_FORMAT, language, 400
            )

        if Users.objects.filter(email=email).exists():
            return ResponseService.create_error_response(
                Messages.EMAIL_ALREADY_EXISTS, language, 400
            )
        if Users.objects.filter(username=username).exists():
            return ResponseService.create_error_response(
                Messages.USERNAME_ALREADY_EXISTS, language, 400
            )

        try:
            hashed_password = make_password(password)
            user = Users.objects.create(
                username=username,
                email=email,
                password=hashed_password,
                is_active=False,
            )

            token = str(uuid.uuid4())

            MailTokens.objects.create(
                user=user,
                token=token,
                type="verify",
                expiration=TokenService.create_expiration_date(60 * 24),  # 1 gün
            )

            send_verification_email(user, token)

            return ResponseService.create_response(
                True, "success", Messages.USER_CREATED_SUCCESSFULLY, language, 201
            )

        except Exception as e:
            logger.error(f"Error during signup: {str(e)}")
            return ResponseService.create_error_response(
                Messages.SIGNUP_FAILED, language, 500
            )

    return ResponseService.create_error_response(
        Messages.INVALID_REQUEST_METHOD, language, 405
    )


def signin(request):
    language = request.headers.get("Accept-Language", "en")
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        signin = data.get("signin")
        password = data.get("password")

        try:
            user = (
                Users.objects.get(email=signin)
                if "@" in signin
                else Users.objects.get(username=signin)
            )
        except Users.DoesNotExist:
            return ResponseService.create_error_response(
                Messages.USER_NOT_FOUND, language, 400
            )

        if not user.is_active:
            return ResponseService.create_error_response(
                Messages.UNACTIVATE_ACCOUNT, language, 400
            )

        if not user.check_password(password):
            return ResponseService.create_error_response(
                Messages.INVALID_CREDENTIALS, language, 400
            )

        access_token, access_exp = TokenService.generate_access_token(user.email)
        refresh_token, refresh_exp = TokenService.generate_refresh_token(user.email)

        token = {
            "access_token": {"token": access_token, "expiration_date": access_exp},
            "refresh_token": {
                "token": refresh_token,
                "expiration_date": refresh_exp,
            },
        }
        user.refresh_token = refresh_token
        user.access_token = access_token
        user.save()
        return ResponseService.create_success_response(token)

    return ResponseService.create_error_response(
        Messages.INVALID_REQUEST_METHOD, language, 405
    )


def signout(request):
    language = request.headers.get("Accept-Language", "en")
    if request.method == "GET":
        try:
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                access_token = auth_header.split(" ")[1]  # "Bearer" kısmını çıkarıyoruz
            else:
                return ResponseService.create_error_response(
                    Messages.INVALID_ACCESS_TOKEN, language, 400
                )

            user = Users.objects.get(access_token=access_token)

            user.refresh_token = None
            user.access_token = None
            user.save()

            return ResponseService.create_response(
                True, "success", Messages.USER_LOGGED_OUT_SUCCESSFULLY, language, 200
            )

        except Users.DoesNotExist:
            return ResponseService.create_error_response(
                Messages.INVALID_ACCESS_TOKEN, language, 400
            )
        except Exception as e:
            logger.error(f"Error during signout: {str(e)}")
            return ResponseService.create_error_response(
                Messages.SIGNOUT_FAILED, language, 500
            )

    return ResponseService.create_error_response(
        Messages.INVALID_REQUEST_METHOD, language, 405
    )


def refreshToken(request):
    language = request.headers.get("Accept-Language", "en")
    if request.method == "GET":
        try:
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                refresh_token = auth_header.split(" ")[1]
            else:
                return ResponseService.create_error_response(
                    Messages.INVALID_REFRESH_TOKEN, language, 400
                )

            user = Users.objects.get(refresh_token=refresh_token)

            if not TokenService.validate_refresh_token(refresh_token):
                return ResponseService.create_error_response(
                    Messages.EXPIRED_OR_INVALID_REFRESH_TOKEN, language, 401
                )

            new_access_token, access_exp = TokenService.generate_access_token(
                user.email
            )
            new_refresh_token, refresh_exp = TokenService.generate_refresh_token(
                user.email
            )

            user.access_token = new_access_token
            user.refresh_token = new_refresh_token
            user.save()

            token = {
                "access_token": {
                    "token": new_access_token,
                    "expiration_date": access_exp,
                },
                "refresh_token": {
                    "token": new_refresh_token,
                    "expiration_date": refresh_exp,
                },
            }
            return ResponseService.create_success_response(token)

        except Users.DoesNotExist:
            return ResponseService.create_error_response(
                Messages.INVALID_REFRESH_TOKEN, language, 400
            )
        except Exception as e:
            logger.error(f"Error during refresh_token: {str(e)}")
            return ResponseService.create_error_response(
                Messages.REFRESH_TOKEN_FAILED, language, 500
            )

    return ResponseService.create_error_response(
        Messages.INVALID_REQUEST_METHOD, language, 405
    )


def verifyAccount(request, verify_token):
    try:
        language = request.headers.get("Accept-Language", "en")
        mail_token = MailTokens.objects.get(
            token=verify_token, type="verify", status=True
        )

        if TokenService.is_mail_token_expired(mail_token.expiration):
            mail_token.status = False
            mail_token.save()

            new_token = str(uuid.uuid4())
            MailTokens.objects.create(
                user=mail_token.user,
                token=new_token,
                type="verify",
                expiration=TokenService.create_expiration_date(60 * 24),
            )

            send_verification_email(mail_token.user, new_token)

            return ResponseService.create_error_response(
                Messages.TOKEN_EXPIRED_NEW_SENT, language, 400
            )

        user = mail_token.user
        user.is_active = True
        user.save()

        mail_token.status = False
        mail_token.save()

        return ResponseService.create_response(
            True, "success", Messages.ACCOUNT_VERIFIED_SUCCESSFULLY, language, 200
        )
    except MailTokens.DoesNotExist:
        return ResponseService.create_error_response(
            Messages.INVALID_OR_EXPIRED_VERIFICATION_TOKEN, language, 400
        )
    except Exception as e:
        logger.error(f"Error during account verification: {str(e)}")
        return ResponseService.create_error_response(
            "error", Messages.AN_ERROR_OCCURRED, language, 500
        )


def intra(request):
    return ResponseService.create_success_response(
        {"url": os.environ.get("INTRA_REDIRECT_URL")}
    )


def intraCallback(request):
    language = request.headers.get("Accept-Language", "en")
    data = json.loads(request.body.decode("utf-8"))
    code = data.get("code")

    if not code:
        return ResponseService.create_error_response(
            Messages.AUTHORIZATION_CODE_NOT_PROVIDED, language, 400
        )

    api_url = os.environ.get("INTRA_API_URL")
    token_url = api_url + "/oauth/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": os.environ.get("INTRA_UID"),
        "client_secret": os.environ.get("INTRA_SECRET"),
        "code": code,
        "redirect_uri": os.environ.get("INTRA_CALLBACK_URL"),
    }

    response = requests.post(token_url, data=payload)
    if response.status_code != 200:
        return ResponseService.create_error_response(
            Messages.FAILED_TO_RETRIEVE_TOKEN, language, response.status_code
        )

    token_data = response.json()
    access_token = token_data.get("access_token")

    user_info_url = api_url + "/v2/users/me"
    headers = {"Authorization": f"Bearer {token_data.get('access_token')}"}

    user_response = requests.request("GET", user_info_url, headers=headers)

    logger.fatal("+++++++++++++++++++++++++++++++++++++++++")
    logger.fatal("Requesting user info from " + user_info_url)
    logger.fatal("token data " + str(token_data))
    logger.fatal("access_token " + access_token)
    logger.fatal("user response " + str(user_response))
    logger.fatal("+++++++++++++++++++++++++++++++++++++++++")

    if user_response.status_code != 200:
        # return JsonResponse({"access_token" : access_token}, status=user_response.status_code)
        return ResponseService.create_error_response(
            Messages.FAILED_TO_RETRIEVE_USER, language, user_response.status_code
        )

    user_data = user_response.json()

    return ResponseService.create_success_response(user_data)
