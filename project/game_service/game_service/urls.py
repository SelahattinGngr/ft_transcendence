from django.urls import path
from src import views

urlpatterns = [
    # Game URLs
    path('games/', views.GameListView.as_view(), name='game-list'),
    path('games/<str:game_id>/', views.GameDetailView.as_view(), name='game-detail'),
    path('games/create/', views.GameCreateView.as_view(), name='game-create'),
    path('games/<str:game_id>/update/', views.GameUpdateView.as_view(), name='game-update'),

    # Move URLs
    path('games/<str:game_id>/moves/', views.MoveCreateView.as_view(), name='move-create'),

    # Tournament URLs
    path('tournaments/', views.TournamentListView.as_view(), name='tournament-list'),
    path('tournaments/create/', views.TournamentCreateView.as_view(), name='tournament-create'),

    # Matchmaking URLs
    path('matchmaking/', views.MatchmakingCreateView.as_view(), name='matchmaking-create'),
    path('matchmaking/status/', views.MatchmakingStatusView.as_view(), name='matchmaking-status'),
]
