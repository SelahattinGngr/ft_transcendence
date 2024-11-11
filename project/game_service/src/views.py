from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Game, Tournament, TournamentGame, Player, Match, MatchScore, GameReplay
from .serializers import GameSerializer, TournamentSerializer, TournamentGameSerializer, MatchSerializer, MatchScoreSerializer, GameReplaySerializer

# Oyun listeleme ve oyun oluşturma
class GameListCreateAPIView(APIView):
    def get(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Turnuva listeleme ve turnuva oluşturma
class TournamentListCreateAPIView(APIView):
    def get(self, request):
        tournaments = Tournament.objects.all()
        serializer = TournamentSerializer(tournaments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TournamentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Belirli bir turnuvaya ait oyunları listeleme
class TournamentGamesAPIView(APIView):
    def get(self, request, tournament_id):
        tournament = Tournament.objects.get(id=tournament_id)
        tournament_games = TournamentGame.objects.filter(tournament_id=tournament)
        serializer = TournamentGameSerializer(tournament_games, many=True)
        return Response(serializer.data)

# Maç ve Skorlar
class MatchListCreateAPIView(APIView):
    def get(self, request):
        matches = Match.objects.all()
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Skorları eklemek veya güncellemek için
class MatchScoreAPIView(APIView):
    def get(self, request, match_id):
        scores = MatchScore.objects.filter(match_id=match_id)
        serializer = MatchScoreSerializer(scores, many=True)
        return Response(serializer.data)

    def post(self, request, match_id):
        data = request.data
        data['match_id'] = match_id
        serializer = MatchScoreSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Oyun Tekrarları (Game Replay)
class GameReplayAPIView(APIView):
    def get(self, request, match_id):
        replays = GameReplay.objects.filter(match_id=match_id)
        serializer = GameReplaySerializer(replays, many=True)
        return Response(serializer.data)

    def post(self, request, match_id):
        data = request.data
        data['match_id'] = match_id
        serializer = GameReplaySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Kullanıcıya ait oyunları listeleme
class UserGamesListView(APIView):
    def get(self, request, user_id):
        # Kullanıcıya ait oyunları player1_id ve player2_id'ye göre filtreliyoruz
        games_player1 = Game.objects.filter(player1_id=user_id)
        games_player2 = Game.objects.filter(player2_id=user_id)
        # Kullanıcıya ait oyunları birleştirip sıralıyoruz
        games = games_player1 | games_player2
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
