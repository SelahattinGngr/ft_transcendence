
from django.urls import path
from src import views

urlpatterns = [
    path('user/create/', views.create_user),
    path('user/intra_create/', views.intra_create),
    path('user/update/<str:username>/', views.update_profile),
    path('user/<str:username>/', views.get_user),
]
