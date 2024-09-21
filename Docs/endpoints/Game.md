# GAME

#### POST /api/v1/game/start

```
Request
Authorization: AccessToken
Content-Type: application/json
{
    "matchId": "", # Burayı backend oluşturacak eşleştirdiğinde
    "players": [
        {
            "userId": "1001",
            "username": "PlayerOne"
        },
        {
            "userId": "1002",
            "username": "PlayerTwo"
        }
    ]
    "gameType": "1v1"  # Oyun türü, birebir oyun modunu belirler
}
```

```
Response
{
    status: true || false,
    status_code: 200 || 400,
    data: {
        "gameId": "",  # Oyun ID'si
        "status": true || false # false ise oynandı ya da oyun yarım kaldı falan
    }
}
```

#### POST /api/v1/game/{gameId}/end

```
Request
Authorization: AccessToken
Content-Type: application/json
{
    "score": {
        "player1": 0,
        "player2": 1
    }
}
```

```
Response
{
    status: true || false,
    status_code: 200 || 400,
    data: {
        "gameId": "",
        "status": "Completed",
        "winner": {
            "userId": "1002",
            "username": "PlayerTwo"
        }
    }
}
```

#### GET /api/v1/game/{gameId}

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
        "gameId": "",
        "status": "InProgress" || "Completed",
        "score": {
            "player1": 0,
            "player2": 1
        }
    }
}
```
