from django.db import models


class Game(models.Model):
    id = models.AutoField(primary_key=True)
    player1_id = models.CharField(max_length=50)
    player2_id = models.CharField(max_length=50)
    winner_id = models.CharField(max_length=50, null=True, blank=True)
    loser_id = models.CharField(max_length=50, null=True, blank=True)
    score_player1 = models.IntegerField()
    score_player2 = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("ongoing", "Ongoing"),
            ("finished", "Finished"),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Game {self.id} - {self.status}"


class Tournament(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("upcoming", "Upcoming"),
            ("ongoing", "Ongoing"),
            ("completed", "Completed"),
        ],
    )
    winner_id = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TournamentGame(models.Model):
    id = models.AutoField(primary_key=True)
    tournament_id = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    round_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tournament {self.tournament_id.name} - Game {self.game_id.id} Round {self.round_number}"


class Player(models.Model):
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="players")
    username = models.CharField(max_length=50)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.username} - {self.game_id.name}"


class Match(models.Model):
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="matches")
    player_1 = models.CharField(max_length=50)
    player_2 = models.CharField(max_length=50)
    winner = models.CharField(max_length=50, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.game_id.name} - {self.player_1} vs {self.player_2}"


class MatchScore(models.Model):
    match_id = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="scores")
    player_username = models.CharField(max_length=50)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.match_id} - {self.player_username}: {self.score}"


class GameReplay(models.Model):
    match_id = models.ForeignKey(
        Match, on_delete=models.CASCADE, related_name="replays"
    )
    replay_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Replay for match {self.match_id.id}"
