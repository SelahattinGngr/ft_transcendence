from django.urls import path
from src.views import GameListCreateAPIView, TournamentListCreateAPIView, TournamentGamesAPIView, MatchListCreateAPIView, MatchScoreAPIView, GameReplayAPIView, UserGamesListView

urlpatterns = [
    # Oyunlar için
    path('games/', GameListCreateAPIView.as_view(), name='game-list-create'),  # Oyunları listeleme ve oluşturma
    path('games/user/<str:user_id>/', UserGamesListView.as_view(), name='user-games-list'),  # Kullanıcıya ait oyunları listeleme

    # Turnuvalar için
    path('tournaments/', TournamentListCreateAPIView.as_view(), name='tournament-list-create'),  # Turnuvaları listeleme ve oluşturma
    path('tournaments/<int:tournament_id>/games/', TournamentGamesAPIView.as_view(), name='tournament-games'),  # Belirli bir turnuvaya ait oyunları listeleme

    # Maçlar ve Skorlar için
    path('matches/', MatchListCreateAPIView.as_view(), name='match-list-create'),  # Maçları listeleme ve oluşturma
    path('matches/<int:match_id>/scores/', MatchScoreAPIView.as_view(), name='match-scores'),  # Skorları eklemek veya güncellemek için

    # Oyun tekrarları (Replay) için
    path('matches/<int:match_id>/replays/', GameReplayAPIView.as_view(), name='game-replay'),  # Oyun tekrarlarını listeleme ve ekleme
]
