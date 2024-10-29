# views.py

import json
from django.views.decorators.csrf import csrf_exempt
from .models import friend_requests
from .ResponseService import ResponseService
from .Messages import Messages

@csrf_exempt
def send_friend_request(request):
    language = request.headers.get("Accept-Language", "en")
    
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        friend_id = data.get('friend_id')
        
        if user_id == friend_id:
            return ResponseService.create_error_response(Messages.CANNOT_ADD_SELF, language, 400)

        # Check if request already exists
        if friend_requests.objects.filter(user_id=user_id, friend_id=friend_id).exists():
            return ResponseService.create_error_response(Messages.REQUEST_ALREADY_EXISTS, language, 400)
        
        friend_requests.objects.create(
            user_id_id=user_id,
            friend_id_id=friend_id,
            status='pending'
        )
        return ResponseService.create_success_response(Messages.REQUEST_SENT_SUCCESS, language, 201)
    
    return ResponseService.create_error_response(Messages.INVALID_METHOD, language, 405)

@csrf_exempt
def respond_to_friend_request(request):
    language = request.headers.get("Accept-Language", "en")
    
    if request.method == 'PUT':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        friend_id = data.get('friend_id')
        status = data.get('status')

        if status not in ['accepted', 'rejected']:
            return ResponseService.create_error_response(Messages.INVALID_STATUS, language, 400)
        
        friend_request = friend_requests.objects.filter(user_id=friend_id, friend_id=user_id, status='pending').first()
        if friend_request is None:
            return ResponseService.create_error_response(Messages.NO_PENDING_REQUEST, language, 404)

        friend_request.status = status
        friend_request.save()

        if status == 'accepted':
            return ResponseService.create_success_response(Messages.REQUEST_ACCEPTED, language, 200)
        else:
            return ResponseService.create_success_response(Messages.REQUEST_REJECTED, language, 200)

    return ResponseService.create_error_response(Messages.INVALID_METHOD, language, 405)

def list_friends(request, user_id):
    language = request.headers.get("Accept-Language", "en")
    
    if request.method == 'GET':
        friends = friend_requests.objects.filter(user_id=user_id, status='accepted')
        friend_list = [
            {
                'friend_id': f.friend_id.id,
                'username': f.friend_id.username,
                'email': f.friend_id.email,
            }
            for f in friends
        ]
        return ResponseService.create_success_response(friend_list, language, 200)

    return ResponseService.create_error_response(Messages.INVALID_METHOD, language, 405)
