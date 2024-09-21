# MAİL

#### POST /api/v1/mail/send-mail

```
request
{
    email:"",
    mail_value:""
}
```

```
response
{
    status:true || false,
    status_code:200 || 400,
    data: {
        message:"mail başarıyla gönderildi"
    }
}
```
