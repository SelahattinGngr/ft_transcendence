# USER

#### GET /api/v1/user/{userId}

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
        user : {
            user_id:"",
            username:"",
            first_name:"",
            last_name:"",
            avatar_url:"",
            bio:"",
            stats: {
                wins:0,
                losses:0
            }
        }
    }
}
```

#### GET /api/v1/user/{userId}/matches

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
        user_matches : {
            user_id:"",
            username:"",
            matches: [
                matches_1: {
                    user_1: {
                        user_id: "",
                        username:""
                    },
                    user_2: {
                        user_id: "",
                        username:""
                    }
                }
            ]
        }
    }
}
```

#### PUT /api/v1/user/{userId}

```
request
Authorization: AccessToken
Content-Type: application/json
{
    bio:"",
    avatar_url:""
}
```

```
response
{
    status:true || false,
    status_code:200 || 400,
    data: {
        user : {
            user_id:"",
            username:"",
            first_name:"",
            last_name:"",
            avatar_url:"",
            bio:"",
            stats: {
                wins:0,
                losses:0
            }
        }
    }
}
```
