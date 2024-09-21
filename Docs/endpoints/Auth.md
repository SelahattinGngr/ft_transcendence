# AUTH

#### POST /api/v1/auth/sigin

```
request
Content-Type: application/json
{
    sign:"email or username",
    password: "password"
}
```

```
response
{
    status:true || false,
    status_code:200 || 400,
    data: {
        user : {
            first_name:"",
            last_name:"",
            refresh_token: {
                token:"",
                expiration_date:"timestamp"
            },
            access_token:{
                token:"",
                expiration_date:"timestamp"
            }
        }
    }
}
```

#### POST /api/v1/auth/signup

```
request
Content-Type: application/json
{
    first_name:"",
    last_name:"",
    email:"",
    password:""
}
```

```
response
{
    status:true || false,
    status_code:200 || 400,
    data: {
        mesagge:""
    }
}
```

#### POST /api/v1/auth/intra

```
request
```

```
response
```

#### GET /api/v1/auth/intra-callback

```
request
```

```
response
```

#### GET /api/v1/auth/signout

```
request
Authorization: RefreshToken
```

```
response
{
    status:true || false,
    status_code:200 || 400,
    data: {
        mesagge:""
    }
}
```

#### GET /api/v1/auth/refresh-token

```
request
Authorization: RefreshToken
```

```
response
{
    status:true || false,
    status_code:200 || 400,
    data: {
        refresh_token: {
            token:"",
            expiration_date:"timestamp"
        },
        access_token:{
            token:"",
            expiration_date:"timestamp"
        }
    }
}
```

#### GET /api/v1/auth/verify-account/{verify-token}

```
request
    - gönderilecek bir şey yok
```

```
response
{
    status:true || false,
    status_code:200 || 400,
    data: {
        mesagge:""
    }
}
```

- reset-password ve forgot-password endpointleri eklenecek
