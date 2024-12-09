from django.db import models

class SavedLog(models.Model):
    id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=100, blank=True)
    log = models.TextField()
    log_ip = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)
