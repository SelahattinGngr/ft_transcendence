import json
import logging
import uuid

from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import MailTokens, Users
from .messages import Messages, get_message

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

def create_json(status, message_enum, language, status_code):
    response_data = {
        "status": status,
        "message": get_message(message_enum, language)
    }
    # ensure_ascii=False ile Unicode karakterlerin kaçış yapılmasını engelle
    return JsonResponse(response_data, status=status_code, json_dumps_params={'ensure_ascii': False})


def signup(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        language = request.headers.get("Accept-Language", "en")
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        # Kullanıcı var mı kontrolü
        if Users.objects.filter(email=email).exists():
            return create_json("error", Messages.EMAIL_ALREADY_EXISTS, language, 400)
        if Users.objects.filter(username=username).exists():
            return create_json("error", Messages.USERNAME_ALREADY_EXISTS, language, 400)

        # Şifreyi hash'leyip kullanıcı oluşturma
        hashed_password = make_password(password)
        user = Users.objects.create(
            username=username,
            email=email,
            password=hashed_password,
            is_active=False,  # Kullanıcı doğrulama e-postası alana kadar pasif olacak
        )

        # E-posta doğrulama tokenı oluşturma
        token = str(uuid.uuid4())[:8]
        MailTokens.objects.create(user=user, token=token, type="verify")

        # E-posta gönderimi
        send_verification_email(user, token)

        return create_json("success", Messages.USER_CREATED_SUCCESSFULLY, language, 201)

    return create_json("error", Messages.INVALID_REQUEST_METHOD, language, 405)


def signin(request):
    return JsonResponse({"message": "Hello from auth service!"})


def intra(request):
    return JsonResponse({"message": "Hello from auth service!"})


def intraCallback(request):
    return JsonResponse({"message": "Hello from auth service!"})


def signout(request):
    return JsonResponse({"message": "Hello from auth service!"})


def refreshToken(request):
    return JsonResponse({"message": "Hello from auth service!"})


def verifyAccount(request, verify_token):
    try:
        mail_token = MailTokens.objects.get(token=verify_token, type="verify", status=True)
        language = request.headers.get("Accept-Language", "en")
        user = mail_token.user
        user.is_active = True
        user.save()

        mail_token.status = False  # Token artık kullanılmayacak
        mail_token.save()

        return create_json("success", Messages.ACCOUNT_VERIFIED_SUCCESSFULLY, language, 200)
    except MailTokens.DoesNotExist:
        return create_json("error", Messages.INVALID_OR_EXPIRED_VERIFICATION_TOKEN, language, 400)
    except Exception as e:
        logger.error(f"Error during account verification: {str(e)}")
        return create_json("error", Messages.AN_ERROR_OCCURRED, language, 500)
