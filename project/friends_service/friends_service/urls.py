from django.urls import path
from src import views

urlpatterns = [
    path("friends/send-request/", views.send_friend_request),
    path("friends/reject-request/<int:id>", views.reject_to_friend_request),
    path("friends/accept-request/<int:id>", views.accept_friend_request),
]
