from django.db import models

class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    receiver_username = models.CharField(max_length=50)
    sender_username = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    content = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)