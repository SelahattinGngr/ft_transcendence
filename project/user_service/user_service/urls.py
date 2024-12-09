
from django.urls import path
from src import views

urlpatterns = [
    path('user/create/', views.create_user),
    path('user/intra_create/', views.intra_create),
    path('user/add_friend/', views.add_friend),
    path('user/list_friends/', views.list_friends),
    path('user/update/<str:username>/', views.update_profile),
    path('user/<str:username>/', views.get_user),
]
