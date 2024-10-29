from django.db import models


class friend_requests(models.Model):
    REQUEST_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    id = models.AutoField(primary_key=True)
    sender_username = models.CharField(max_length=255)
    receiver_username = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=REQUEST_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
