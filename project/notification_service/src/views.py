import logging

from django.http import JsonResponse

logger = logging.getLogger(__name__)

def deneme(request):
    logger.fatal('This is a fatal log message')
    return JsonResponse({'message': 'Hello, World!'})