from django.db import models

class Game(models.Model):
    game_id = models.CharField(max_length=100, unique=True)
    player1_id = models.CharField(max_length=100)  # User servisinden gelen user_id
    player1_username = models.CharField(max_length=100)
    player2_id = models.CharField(max_length=100)  # User servisinden gelen user_id
    player2_username = models.CharField(max_length=100)
    state = models.JSONField()  # Oyunun durumu JSON formatında tutulur
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.player1_username} vs {self.player2_username}"


class Move(models.Model):
    move_id = models.AutoField(primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='moves')
    player_id = models.CharField(max_length=100)  # Hareketi yapan oyuncunun user_id'si
    player_username = models.CharField(max_length=100)
    move_details = models.JSONField()  # Hamlenin detayı JSON formatında
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Move {self.move_id} by {self.player_username} in Game {self.game.game_id}"
