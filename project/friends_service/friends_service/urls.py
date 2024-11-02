from django.urls import path
from src import views

urlpatterns = [
    path("friend/send-request/", views.send_friend_request),
    path("friend/reject-request/<int:id>", views.reject_to_friend_request),
    path("friend/accept-request/<int:id>", views.accept_friend_request),
]
