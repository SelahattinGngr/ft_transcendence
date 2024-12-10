from django.db import models

class GameHistory(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    userScore= models.IntegerField()
    ainame = models.CharField(max_length=20, unique=True)
    aiScore = models.IntegerField()
    isWin = models.BooleanField(default=True)