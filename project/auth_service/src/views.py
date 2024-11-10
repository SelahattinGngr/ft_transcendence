import json
import logging
import os
import uuid

import requests
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .KafkaProducer import send_kafka_message

from .Messages import Messages
from .models import MailTokens, Users
from .ResponseService import ResponseService
from .TokenService import TokenService

logger = logging.getLogger(__name__)


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
            try:
                send_kafka_message(
                    "user-registration-events", {"email": email, "token": f"http://localhost:8000/auth/verify-account/{token}"}
                )
                logger.fatal(f"Verification email sent to {email}")
            except Exception as e:
                logger.error(f"Error during sending verification email: {str(e)}")

            # UserService'e kullanıcıyı kaydetme
            user_service_url = os.environ.get("USER_SERVICE_URL")
            user_create_url = f"{user_service_url}/user/create/"
            headers = {"Accept-Language": language, "Accept": "application/json"}
            user_data = {
                "username": username,
                "email": email,
                "first_name": data.get("first_name", ""),
                "last_name": data.get("last_name", ""),
                "source_id": user.id,
                "avatar_url": data.get("avatar_url", ""),
            }
            user_service_response = requests.post(
                user_create_url, json=user_data, headers=headers
            )
            if user_service_response.status_code != 201:
                user.delete()  # Eğer UserService kaydetmede hata alırsa, auth service'deki kullanıcıyı sil.
                return ResponseService.create_error_response(
                    Messages.USER_CREATION_FAILED, language, 500
                )

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

        access_token, access_exp = TokenService.generate_access_token(user.username)
        refresh_token, refresh_exp = TokenService.generate_refresh_token(user.username)

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
                user.username
            )
            new_refresh_token, refresh_exp = TokenService.generate_refresh_token(
                user.username
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

            # send_verification_email(mail_token.user, new_token)

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
            Messages.AN_ERROR_OCCURRED, language, 500
        )


def validate_token(request):
    language = request.headers.get("Accept-Language", "en")
    if request.method == "GET":
        access_token = request.headers.get("Authorization")
        refresh_token = request.headers.get("Refresh")

        if not access_token and not refresh_token:
            return ResponseService.create_error_response(
                Messages.MISSING_TOKEN, language, status_code=400
            )

        if access_token and TokenService.validate_access_token(access_token):
            return ResponseService.create_success_response({"valid": True})

        if refresh_token and TokenService.validate_refresh_token(refresh_token):
            return ResponseService.create_success_response({"valid": True})

        return ResponseService.create_error_response(
            Messages.INVALID_OR_EXPIRED_VERIFICATION_TOKEN, language, status_code=401
        )

    return ResponseService.create_error_response(
        Messages.INVALID_REQUEST_METHOD, language, status_code=405
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
        "grant_type": "authorization_code",
        "client_id": os.environ.get("INTRA_UID"),
        "client_secret": os.environ.get("INTRA_SECRET"),
        "code": code,
        "redirect_uri": os.environ.get("INTRA_CALLBACK_URL"),
    }

    response = requests.post(token_url, data=payload)
    logger.fatal(f"Response from token endpoint: {response.json()}")
    if response.status_code != 200:
        return ResponseService.create_error_response(
            Messages.FAILED_TO_RETRIEVE_TOKEN, language, response.status_code
        )

    token_data = response.json()
    access_token = token_data.get("access_token")

    user_response = intra_user(api_url, access_token)
    if user_response.status_code != 200 and user_response.status_code != 201:
        return ResponseService.create_error_response(
            Messages.FAILED_TO_RETRIEVE_USER, language, str(user_response.json())
        )

    return user_response


def intra_user(api_url, access_token):
    user_info_url = api_url + "/v2/me"
    headers = {"Authorization": f"Bearer {access_token}"}

    user_response = requests.request("GET", user_info_url, headers=headers)
    if user_response.status_code != 200:
        return user_response

    json_data = user_response.json()
    user_service_url = os.environ.get("USER_SERVICE_URL")
    user_create_data = {
        "username": json_data.get("login"),
        "email": json_data.get("email"),
        "first_name": json_data.get("first_name"),
        "last_name": json_data.get("last_name"),
        "source": "intra",
        "source_id": json_data.get("id"),
        "avatar_url": json_data.get("image"),
    }

    # Kullanıcı daha önce oluşturulmuşsa bilgileri getir
    user = Users.objects.filter(username=user_create_data["username"]).first()
    if user:
        return ResponseService.create_success_response(
            valid_user(user, user_service_url), 200
        )

    # Kullanıcı daha önce oluşturulmamışsa oluştur

    return ResponseService.create_success_response(
        invalid_user(user_service_url, user_create_data), 201
    )


def create_tokens(username):
    rtoken, exp = TokenService.generate_refresh_token(username)
    atoken, exp = TokenService.generate_access_token(username)
    refresh_token = {"token": rtoken, "expiration_date": exp}
    access_token = {"token": atoken, "expiration_date": exp}
    return refresh_token, access_token


def valid_user(user, user_service_url):
    user_get_url = f"{user_service_url}/user/{user.username}"
    request = requests.get(user_get_url)
    data = request.json()
    data["refresh_token"], data["access_token"] = create_tokens(user.username)
    user.refresh_token = data["refresh_token"]["token"]
    user.access_token = data["access_token"]["token"]
    user.save()
    return data


def invalid_user(user_service_url, user_create_data):
    user_create_url = f"{user_service_url}/user/intra_create/"
    request = requests.post(user_create_url, json=user_create_data)
    data = request.json()
    data["refresh_token"], data["access_token"] = create_tokens(
        user_create_data["username"]
    )
    user = Users.objects.create(
        username=user_create_data["username"],
        email=user_create_data["email"],
        is_active=True,
        refresh_token=data["refresh_token"]["token"],
        access_token=data["access_token"]["token"],
    )
    return data


# diger servislerden access token uzerinden username almak icin kullanilacak
def get_accesstoken_by_username(request):
    language = request.headers.get("Accept-Language", "en")
    if request.method == "GET":
        access_token = request.headers.get("Authorization")
        if not access_token:
            return ResponseService.create_error_response(
                Messages.MISSING_TOKEN, language, status_code=400
            )
        username = TokenService.validate_access_token(access_token.split(" ")[1])
        if not username:
            return ResponseService.create_error_response(
                Messages.INVALID_ACCESS_TOKEN, language, status_code=400
            )
        logger.fatal(f"Username retrieved by access token: {username}")
        user = Users.objects.filter(username=username).first()
        if not user:
            return ResponseService.create_error_response(
                Messages.USER_NOT_FOUND, language, status_code=400
            )
        return ResponseService.create_success_response({"username": user.username}, 200)

    return ResponseService.create_error_response(
        Messages.INVALID_REQUEST_METHOD, language, status_code=405
    )

def retry_verification_account(request):
    language = request.headers.get("Accept-Language", "en")
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        email = data.get("email")
        try:
            user = Users.objects.get(email=email)
            mail_token = MailTokens.objects.get(user=user, type="verify", status=True)
            if TokenService.is_mail_token_expired(mail_token.expiration):
                mail_token.status = False
                mail_token.save()

                new_token = str(uuid.uuid4())
                MailTokens.objects.create(
                    user=user,
                    token=new_token,
                    type="verify",
                    expiration=TokenService.create_expiration_date(60 * 24),
                )

                # send_verification_email(mail_token.user, new_token)

                return ResponseService.create_error_response(
                    Messages.TOKEN_EXPIRED_NEW_SENT, language, 400
                )

            try:
                send_kafka_message(
                    "user-registration-events", {"email": email, "token": f"http://localhost:8000/auth/verify-account/{mail_token.token}"}
                )
                logger.fatal(f"Verification email sent to {email}")
            except Exception as e:
                logger.error(f"Error during sending verification email: {str(e)}")

            return ResponseService.create_response(
                True, "success", Messages.VERIFICATION_EMAIL_SENT, language, 200
            )
        except Users.DoesNotExist:
            return ResponseService.create_error_response(
                Messages.USER_NOT_FOUND, language, 400
            )
        except MailTokens.DoesNotExist:
            return ResponseService.create_error_response(
                Messages.INVALID_OR_EXPIRED_VERIFICATION_TOKEN, language, 400
            )
        except Exception as e:
            logger.error(f"Error during retry_verification_email: {str(e)}")
            return ResponseService.create_error_response(
                Messages.AN_ERROR_OCCURRED, language, 500
            )

    return ResponseService.create_error_response(
        Messages.INVALID_REQUEST_METHOD, language, 405
    )