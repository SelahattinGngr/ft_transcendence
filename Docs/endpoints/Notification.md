# NOTIFICATION

#### POST /api/v1/notifications/send

```
Request
Content-Type: application/json
{
    "recipientUserId": "",
    "title": "",
    "message": "",
    "type": "info" || "warning" || "error" || "success"
}
```

```
Response
{
    "status": true || false,
    "status_code": 200 || 400,
    "data": {
        "notificationId": "",
        "recipientUserId": "",
        "title": "",
        "message": "",
        "type": "info" || "warning" || "error" || "success",
        "timestamp": "2024-09-01T12:34:56Z"
    }
}
```

#### GET /api/v1/notifications

```
Request
Authorization: AccessToken
```

```
Response
{
    "status": true || false,
    "status_code": 200 || 400,
    "data": [
        {
            "notificationId": "",
            "title": "",
            "message": "",
            "type": "friend_request" || "game_invite" || "tournament_update" || "system_message",
            "timestamp": "2024-09-01T12:34:56Z",
            "isRead": true || false
        }
    ]
}
```

#### PUT /api/v1/notifications/{notificationId}/mark-as-read

```
Request
Authorization: AccessToken
```

```
Response
{
    "status": true || false,
    "status_code": 200 || 400,
    "data": {
        "notificationId": "",
        "isRead": true
    }
}
```

#### DELETE /api/v1/notifications/{notificationId}

```
Request
Authorization: AccessToken
```

```
Response
{
    "status": true || false,
    "status_code": 200 || 400,
    "data": {
        "message": "Notification deleted successfully"
    }
}
```
