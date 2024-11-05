import json
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse

def mail_service(request):
    if request.method == "POST":
        data = json.loads(request.body)
        
        subject = data.get('subject')
        message = data.get('message')
        from_email = settings.EMAIL_HOST_USER
        email = data.get('user_email')
        
        try:
            send_mail(subject, message, from_email, [email])
            return JsonResponse({"message" : "mail recieved successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"message": f"An error occurred: {str(e)}"}, status=500)
            
    else:
        return JsonResponse({"message" : "invalid request"}, status=400)