import json
import logging
import uuid

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

        # E-posta formatı validasyonu
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

            # E-posta gönderimi (hata yönetimi eklenebilir)
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
            user = Users.objects.get(email=signin) if '@' in signin else Users.objects.get(username=signin)
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


def intra(request):
    return ResponseService.create_success_response(
        {"message": "Hello from auth service!"}
    )


def intraCallback(request):
    return ResponseService.create_success_response(
        {"message": "Hello from auth service!"}
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
