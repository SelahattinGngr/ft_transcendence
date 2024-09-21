# FRIENDS

##### POST /api/v1/friends/friend-request

```
request
Authorization: AccessToken
Content-Type: application/json
{
    "target_user":id
}
```

```
response
{
    status:true || false,
    status_code:200 || 400,
    data: {
        "message": "",
    }
}
```

##### POST /api/v1/friends/accept-request

```
request
Authorization: AccessToken
Content-Type: application/json
{
    "target_user":id
}
```

```
response
{
    status:true || false,
    status_code:200 || 400,
    data: {}
}
```

##### POST /api/v1/friends/deny-request

```
request
Authorization: AccessToken
Content-Type: application/json
{
    "target_user":id
}
```

```
response
{
    status:true || false,
    status_code:200 || 400,
    data: {}
}
```
