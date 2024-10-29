from django.urls import path
from src import views

urlpatterns = [
    path("friends/send-request/", views.send_friend_request),
    path("friends/respond-request/", views.respond_to_friend_request),
    path("friends/list/<int:user_id>/", views.list_friends),
]
