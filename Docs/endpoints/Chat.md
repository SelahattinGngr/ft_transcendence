# CHAT

#### POST /api/v1/chat/send

```
request
Authorization: AccessToken
Content-Type: application/json
{
    "target_user":id
    "messages":""
    "conversation_id":id
}
```

```
response
{
    status:true || false,
    status_code:200 || 400,
    data: {
        "message": "message sending",
    }
}
```

#### GET /api/v1/chat/chats

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
        conversation_id: [id1, id2, id3]
    }
}
```

#### GET /api/v1/chat/{conversationId}

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
        conversation_id:id,
        messages: [ # max 50 tane
            message_1: {
                user:id1,
                message:""
            }
            message_2: {
                user:id2,
                message:""
            }
        ]
    }
}
```
