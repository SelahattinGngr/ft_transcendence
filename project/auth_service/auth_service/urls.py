from django.urls import include, re_path
from src import views

urlpatterns = [
    re_path('auth/deneme', views.deneme),
]
