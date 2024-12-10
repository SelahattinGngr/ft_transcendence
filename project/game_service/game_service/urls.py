from django.urls import path
from src import views

urlpatterns = [
    path('game/save-game/', views.save_game),
    path('game/get-history/<str:username>/', views.get_history),
]
