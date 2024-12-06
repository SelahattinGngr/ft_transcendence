from django.db import models

class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    content = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - {self.type}"