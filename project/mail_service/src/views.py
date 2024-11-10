import json
import logging
import os

from django.core.mail import send_mail
from django.http import JsonResponse

logger = logging.getLogger(__name__)

def send_email(email, subject, message):
    from_email = os.getenv("EMAIL_HOST_USER")
    logger.fatal(f"Sending email to {email} with subject '{subject}'")
    logger.fatal("ANANI SIKIYIM ANANI O MESAJ GONDERMEYEN CARIKLI ANANI SIKIYIM")
    try:
        send_mail(subject, message, from_email, [email])
        logger.fatal(f"Email sent to {email} with subject '{subject}'")
    except Exception as e:
        logger.fatal(f"Failed to send email to {email}: {str(e)}")


def mail_service(request):
    if request.method == "POST":
        data = json.loads(request.body)
        
        # Verileri JSON'dan al
        subject = data.get('subject')
        message = data.get('message')
        email = data.get('user_email')
        
        if not all([subject, message, email]):
            return JsonResponse({"message": "Missing email parameters"}, status=400)
        
        # E-posta gönderimi
        send_email(email, subject, message)
        return JsonResponse({"message": "Email sent successfully"}, status=200)

    return JsonResponse({"message": "Invalid request"}, status=400)


# KafkaConsumer.py içinde çağrı örneği
def send_verification_email(email, token):
    subject = "Email Verification"
    message = f"Please verify your email using this token: {token}"
    send_email(email, subject, message)
