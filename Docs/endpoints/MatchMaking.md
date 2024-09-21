# MATCHMAKING

#### POST /api/v1/matchmaking/find-match

```
Request
Authorization: AccessToken
Content-Type: application/json
{
    "tournamentId": "", # nullable true
    "userId": "",  # Oyuncu ID'si
    "gameType": ""  # Oyun türü veya modu
}
```

```
Response
{
    status: true || false,
    status_code: 200 || 400,
    data: {
        "matchId": "",  # Eşleştirme ID'si
        "opponent": {
            "userId": "1002",
            "username": "PlayerTwo"
        }
    }
}
```

#### POST /api/v1/matchmaking/find-matchGET /api/v1/matchmaking/{matchId}

```
Request
Authorization: AccessToken
```

```
Response
{
    status: true || false,
    status_code: 200 || 400,
    data: {
        "matchId": "",
        "opponent": {
            "userId": "1002",
            "username": "PlayerTwo"
        },
        "status": "Pending" || "InProgress" || "Completed",
        "score": {
            "player1": 0,
            "player2": 1
        }
    }
}
```
