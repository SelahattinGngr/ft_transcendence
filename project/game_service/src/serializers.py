from rest_framework import serializers
from .models import Game, Move

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['game_id', 'player1_id', 'player1_username', 'player2_id', 'player2_username', 'state', 'is_active', 'created_at', 'updated_at']

class MoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Move
        fields = ['move_id', 'game', 'player_id', 'player_username', 'move_details', 'created_at']
