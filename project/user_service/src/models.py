from django.db import models


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    avatar_id = models.ForeignKey("Avatar", on_delete=models.CASCADE)
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
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        Users, related_name="friends_of_user", on_delete=models.CASCADE
    )
    friend_id = models.ForeignKey(
        Users, related_name="friends_of_friend", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BlockedUsers(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        Users, related_name="blocked_user", on_delete=models.CASCADE
    )
    blocked_user_id = models.ForeignKey(
        Users, related_name="blocked_by_user", on_delete=models.CASCADE
    )
    username = models.CharField(Users, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
