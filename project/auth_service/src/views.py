from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.

def deneme(request):
    print(request)
    print("deneme")
    return JsonResponse({"message": "Hello from auth service!"})