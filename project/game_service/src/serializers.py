from rest_framework import serializers
from .models import Game, Tournament, TournamentGame, Match, MatchScore, GameReplay

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = '__all__'

class TournamentGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentGame
        fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'

class MatchScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchScore
        fields = '__all__'

class GameReplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = GameReplay
        fields = '__all__'
