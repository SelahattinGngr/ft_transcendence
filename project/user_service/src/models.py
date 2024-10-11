from django.db import models


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    avatar_id = models.ForeignKey('Avatar', on_delete=models.CASCADE)
    source_id = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    bio = models.TextField(max_length=255)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50, null=True)
    status = models.BooleanField(default=True)
    source = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Avatar(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=255)
    large_url = models.CharField(max_length=255)
    medium_url = models.CharField(max_length=255)
    small_url = models.CharField(max_length=255)
    micro_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Friends(models.Model):
    FRIENDS_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, related_name='friends_of_user', on_delete=models.CASCADE)
    friend_id = models.ForeignKey(Users, related_name='friends_of_friend', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=FRIENDS_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)