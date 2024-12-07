from django.db import models

class Saved_log(models.Model):
    id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=100, blank=True)
    log = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    log_ip = models.GenericIPAddressField()
