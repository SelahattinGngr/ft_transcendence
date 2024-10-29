# views.py
import json
import os

import requests

from .Messages import Messages
from .models import friend_requests
from .ResponseService import ResponseService

# arkadaslık isteği gönderme
def send_friend_request(request):
    language = request.headers.get("Accept-Language", "en")
    
    if request.method == 'POST':
        access_token = request.headers.get('Authorization')
        if access_token is None:
            return ResponseService.create_error_response(Messages.NO_ACCESS_TOKEN, language, 401)
        
        auth_service_url = os.environ.get('AUTH_SERVICE_URL')
        access_user = requests.get(f'{auth_service_url}/auth/access-token-by-username/', headers={'Authorization': access_token})
        if access_user.status_code != 200:
            return ResponseService.create_error_response(Messages.INVALID_ACCESS_TOKEN, language, 401)
        
        data = json.loads(request.body)
        username = access_user.json().get('username')
        friend_username = data.get('friend_username')
        
        if username == friend_username:
            return ResponseService.create_error_response(Messages.CANNOT_ADD_SELF, language, 400)

        # Check if request already exists
        if friend_requests.objects.filter(sender_username=username, receiver_username=friend_username).exists():
            return ResponseService.create_error_response(Messages.REQUEST_ALREADY_EXISTS, language, 400)
        
        friend_requests_obj = friend_requests.objects.create(
            sender_username=username,
            receiver_username=friend_username,
            status='pending'
        )
        # Send notification
        # notification_service_url = os.environ.get('NOTIFICATION_SERVICE_URL')
        # requests.post(f'{notification_service_url}/notifications/send/', json={
        #     'receiver_username': friend_username,
        #     'friend_request_id': friend_requests_obj.id,
        #     'message': f'{username} wants to be your friend.'
        # })

        return ResponseService.create_success_response(Messages.REQUEST_SENT_SUCCESS, language, 201)
    
    return ResponseService.create_error_response(Messages.INVALID_METHOD, language, 405)

# arkadaslık isteğine yanıt verme
def reject_to_friend_request(request, id):
    language = request.headers.get("Accept-Language", "en")

    if request.method == 'GET':
        # access token ile kontrol eklenecek
        friend_request = friend_requests.objects.get(id=id)
        friend_request.status = 'rejected'
        friend_request.save()

        return ResponseService.create_success_response(Messages.REQUEST_REJECTED, language, 200)

    return ResponseService.create_error_response(Messages.INVALID_METHOD, language, 405)

# arkadaslık isteğini kabul etme
def accept_friend_request(request, id):
    language = request.headers.get("Accept-Language", "en")

    if request.method == 'GET':
        # access token ile kontrol eklenecek
        friend_request = friend_requests.objects.get(id=id)
        friend_request.status = 'accepted'
        friend_request.save()

        # send notification
        # notification_service_url = os.environ.get('NOTIFICATION_SERVICE_URL')
        # requests.post(f'{notification_service_url}/notifications/send/', json={
        #     'receiver_username': friend_request.sender_username,
        #     'message': f'{friend_request.receiver_username} accepted your friend request.'
        # })

        # bu kısım kafka ile yeniden yazılacak
        user_service_url = os.environ.get('USER_SERVICE_URL')
        requests.post(f'{user_service_url}/user/add-friend/', json={
            'username': friend_request.sender_username,
            'friend_username': friend_request.receiver_username
        })

        return ResponseService.create_success_response(Messages.REQUEST_ACCEPTED, language, 200)

    return ResponseService.create_error_response(Messages.INVALID_METHOD, language, 405)