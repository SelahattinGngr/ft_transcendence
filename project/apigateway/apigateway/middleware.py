from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseNotFound

class RequestRouterMiddleware:
    def __init__(self, get_response):
        print(get_response)
        self.get_response = get_response

    def __call__(self, request):
        # İsteği analiz et
        print('---------------')
        print('Request path:', request.path)
        print('---------------')

        # İsteği yönlendirmek için gerekli kod
        response = self.get_response(request)

        if request.path.startswith('/auth/'):
            print('////////////////')
            print('Auth service')
            print('////////////////')
            return self.get_response(request)
        # Eğer yönlendirme başarılı değilse
        if response.status_code == 404:
            return HttpResponseNotFound("Not Found")

        return response