from django.db import models
from django.contrib.auth.hashers import check_password, make_password

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    refresh_token = models.CharField(max_length=255, null=True)
    access_token = models.CharField(max_length=255, null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def check_password(self, password):
        return check_password(password, self.password)
    
    def set_password(self, password):
        self.password = make_password(password)

class MailTokens(models.Model):
    TOKEN_TYPE_CHOICES = [
        ('verify', 'Verify'),
        ('forgot-password', 'Forgot Password'),
        ('reset-password', 'Reset Password'),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TOKEN_TYPE_CHOICES)
    status = models.BooleanField(default=True)
    expiration = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TwofactorCodes(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    code = models.CharField(max_length=4)
    status = models.BooleanField(default=True)
    expiration = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)