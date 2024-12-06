from django.db import models

class saved_log(models.Model):
    id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=100)
    log = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
