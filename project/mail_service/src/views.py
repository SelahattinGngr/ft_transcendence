import json
import logging
import os

from django.core.mail import send_mail
from django.http import JsonResponse

from .addLog import Log

logger = logging.getLogger(__name__)
service_name = "mail_service"

def send_email(email, subject, message):
    from_email = os.getenv("EMAIL_HOST_USER")
    try:
        send_mail(subject, message, from_email, [email])
        logger.fatal(f"Email sent to {email} with subject '{subject}'")
        Log.add_log(service_name, f"Email sent to {email} with subject '{subject}'", None)
    except Exception as e:
        logger.fatal(f"Failed to send email to {email}: {str(e)}")
        Log.add_log(service_name, f"Failed to send email to {email}: {str(e)}", None)


def mail_service(request):
    if request.method == "POST":
        data = json.loads(request.body)
        
        # Verileri JSON'dan al
        subject = data.get('subject')
        message = data.get('message')
        email = data.get('user_email')
        
        if not all([subject, message, email]):
            Log.add_log(service_name, "Missing email parameters", request)
            return JsonResponse({"message": "Missing email parameters"}, status=400)
        
        # E-posta gönderimi
        send_email(email, subject, message)
        Log.add_log(service_name, f"Email sent to {email} with subject '{subject}'", request)
        return JsonResponse({"message": "Email sent successfully"}, status=200)
    Log.add_log(service_name, "Invalid request", request)
    return JsonResponse({"message": "Invalid request"}, status=400)


# KafkaConsumer.py içinde çağrı örneği
def send_verification_email(email, token):
    subject = "Email Verification"
    message = f"Please verify your email using this token: {token}"
    send_email(email, subject, message)

def send_2fa_email(email, code):
    subject = "2FA Code"
    message = f"Your 2FA code is: {code}"
    send_email(email, subject, message)
