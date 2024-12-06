import os
import requests
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

class TokenValidationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Eğer istek Auth servisine ise token doğrulama yapma
        if request.path.startswith('/auth/'):
            return None

        # Bearer token'ı header'dan al
        auth_header = request.headers.get('Authorization')
        if auth_header is None or not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'Authorization token missing or invalid'}, status=401)

        token = auth_header.split(' ')[1]

        # Auth servisine token doğrulama isteği gönder
        auth_service_url = os.environ.get('AUTH_SERVICE_URL')
        validation_url = f'{auth_service_url}/auth/validate-token/'
        response = requests.get(validation_url, headers={'Authorization': f'Bearer {token}'})

        if response.status_code != 200:
            return JsonResponse({'error': 'Invalid token'}, status=401)

        return None
