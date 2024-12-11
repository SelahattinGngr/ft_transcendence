from django.db import models

class GameHistory(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=False)
    userScore= models.IntegerField()
    aiName = models.CharField(max_length=20, unique=False)
    aiScore = models.IntegerField()
    isWin = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)