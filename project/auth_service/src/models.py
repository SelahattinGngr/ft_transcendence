from django.db import models


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    refresh_token = models.CharField(max_length=50, null=True)
    access_token = models.CharField(max_length=50, null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MailTokens(models.Model):
    TOKEN_TYPE_CHOICES = [
        ('verify', 'Verify'),
        ('forgot-password', 'Forgot Password'),
        ('reset-password', 'Reset Password'),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    token = models.CharField(max_length=20)
    type = models.CharField(max_length=20, choices=TOKEN_TYPE_CHOICES)
    status = models.BooleanField(default=True)
    expiration = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)