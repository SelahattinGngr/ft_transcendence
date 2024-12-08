from re import L
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Game, Move
from .serializers import GameSerializer, MoveSerializer

from .addLog import Log
service_name = "game_service"

"""
    frontend de oyun oynansın backend sadece kimlerin oynadığını ve oyunun durumunu tutsun
    front da oyuncuya davet atılsın kafi
"""

# Game API Views
class GameListView(APIView):
    """
    Liste halinde mevcut tüm oyunları getirir.
    """
    def get(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        Log.add_log(service_name, "Game list retrieved", request)
        return Response(serializer.data)

class GameDetailView(APIView):
    """
    Belirli bir oyunun detaylarını gösterir.
    """
    def get(self, request, game_id):
        game = get_object_or_404(Game, game_id=game_id)
        serializer = GameSerializer(game)
        Log.add_log(service_name, f"Game {game_id} details retrieved", request)
        return Response(serializer.data)

class GameCreateView(APIView):
    """
    Yeni bir oyun başlatır.
    """
    def post(self, request):
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            Log.add_log(service_name, "New game created", request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        Log.add_log(service_name, "Game creation failed", request)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GameUpdateView(APIView):
    """
    Mevcut bir oyunun durumunu günceller (örneğin, oyuncu hamlesi).
    """
    def put(self, request, game_id):
        game = get_object_or_404(Game, game_id=game_id)
        serializer = GameSerializer(game, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            Log.add_log(service_name, f"Game {game_id} updated", request)
            return Response(serializer.data)
        Log.add_log(service_name, f"Game {game_id} update failed", request)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Move API Views
class MoveCreateView(APIView):
    """
    Oyuna yeni bir hamle ekler.
    """
    def post(self, request, game_id):
        game = get_object_or_404(Game, game_id=game_id)
        serializer = MoveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(game=game)
            Log.add_log(service_name, f"New move added to game {game_id}", request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        Log.add_log(service_name, f"Move creation failed in game {game_id}", request)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Tournament API Views
class TournamentCreateView(APIView):
    """
    Yeni bir turnuva oluşturur.
    """
    def post(self, request):
        # Turnuva oluşturma işlemleri
        Log.add_log(service_name, "New tournament created", request)
        return Response({"message": "Turnuva başarıyla oluşturuldu!"}, status=status.HTTP_201_CREATED)

class TournamentListView(APIView):
    """
    Mevcut tüm turnuvaları listeler.
    """
    def get(self, request):
        # Turnuva listesi çekme işlemleri
        Log.add_log(service_name, "Tournament list retrieved", request)
        return Response({"message": "Turnuva listesi burada!"}, status=status.HTTP_200_OK)

# Matchmaking API Views
class MatchmakingCreateView(APIView):
    """
    İki oyuncuyu eşleştirir.
    """
    def post(self, request):
        # Eşleştirme işlemleri
        Log.add_log(service_name, "Matchmaking created", request)
        return Response({"message": "Eşleştirme başarıyla yapıldı!"}, status=status.HTTP_201_CREATED)

class MatchmakingStatusView(APIView):
    """
    Eşleştirme durumunu kontrol eder.
    """
    def get(self, request):
        # Eşleştirme durumu kontrol işlemleri
        Log.add_log(service_name, "Matchmaking status retrieved", request)
        return Response({"message": "Eşleştirme durumu!"}, status=status.HTTP_200_OK)
