
from django.urls import path
from src import views

urlpatterns = [
    path('user/intra_create/', views.intra_create),
]
