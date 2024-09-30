from django.http import JsonResponse
from django.shortcuts import render


def deneme(request):
    return JsonResponse({"message": "Hello from user service!"})