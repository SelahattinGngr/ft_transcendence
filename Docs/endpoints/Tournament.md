# TOURNAMENT

#### POST /api/v1/tournament/create-tournament

```
Request
Authorization: AccessToken
Content-Type: application/json
{
    "name": "",
    "description": "",
    "password":"",
    "maxParticipants": 4 - 8
}
```

```
response
{
    status:true || false,
    status_code:200 || 400,
    data: {
        "tournamentId": "",
        "name": "",
        "description": "",
        "maxParticipants": 4 - 8,
        "gameId": "",
        "status": true || false # turnuva bittiyse false olacak
    }
}
```

#### POST /api/v1/tournament/{tournamentId}/invite

```
request
Authorization: AccessToken
Content-Type: application/json
{
    "inviteeUserId": ""
}
```

```
response
{
    status:true || false,
    status_code:200 || 400,
    data: {
        "message": "",
        "tournamentId": "",
        "inviterUserId": "",
        "inviteeUserId": "",
        "status": "Pending"
    }
}
```

#### POST /api/v1/tournament/{tournamentId}/invitations/{invitationId}/respond

```
request
Authorization: AccessToken
Content-Type: application/json
{
    "response": true || false
}
```

```
response
{
    status:true || false,
    status_code:200 || 400,
    data: {
        "message": "",
        "tournamentId": "",
        "response": true || false
    }
}
```

#### GET /api/v1/tournament/{tournamentId}

```
request
Authorization: AccessToken
```

```
response
{
    status:true || false,
    status_code:200 || 400,
    data: {
        "tournamentId": "",
        "name": "",
        "description": "",
        "maxParticipants": 4 - 8,
        "gameId": [],
        "status": true || false # turnuva bittiyse false olacak
        "participants": [
            {
                "userId": "1001",
                "username": "PlayerOne"
            },
            {
                "userId": "1002",
                "username": "PlayerTwo"
            }
        ]
    }
}
```

#### POST /api/v1/tournament/{tournamentId}/join

```
request
Authorization: AccessToken
Content-Type: application/json
{
    "password":""
}
```

```
response
{
    status:true || false,
    status_code:200 || 400,
    data: {
        "message": "",
        "tournamentId": "",
        "userId": ""
    }
}
```

#### GET /api/v1/tournament/tournaments

```
request
Authorization: AccessToken
```

```
response
{
    status:true || false,
    status_code:200 || 400,
    data: {[
                {
                    "tournamentId": "",
                    "name": "",
                    "status": true
                },
                {
                    "tournamentId": "",
                    "name": "",
                    "status": true
                }
        ]
    }
}
```

#### DELETE /api/v1/tournament/{tournamentId}

```
request
Authorization: AccessToken
```

```
response
{
    status:true || false,
    status_code:200 || 400,
    data: {
        {
            "message": "",
            "tournamentId": "",
            "status": false
        }
    }
}
```

#### GET /api/v1/tournament/start

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
        "message": "Turnuva başlatıldı",
        "tournamentId": "",
        "gameId": ""  # Eşleşme yapılmış oyun ID'si
    }
}
```

#### POST /api/v1/tournament/play

```
request
```

```
response
```
