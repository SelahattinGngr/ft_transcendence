from django.db import models
#from django.contrib.auth.models import User
from django.utils.timezone import localtime


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    first_user_id = models.IntegerField(verbose_name="İlk Kullanıcı ID")
    second_user_id = models.IntegerField(verbose_name="İkinci Kullanıcı ID")

class Message(models.Model):
    user_id = models.IntegerField(verbose_name="Kullanıcı ID")
    room = models.ForeignKey(Room, related_name="messages", verbose_name="Oda", on_delete=models.CASCADE)
    content = models.TextField(verbose_name="Mesaj İçeriği")
    created_at = models.DateTimeField(auto_now_add=True)

    def get_short_date(self):
        local_time = localtime(self.created_at)#django timezone kullanarak tarih ve saat bilgisini al
        return f"{local_time.hour}:{local_time.minute:02d}"
    

"""
class Room(models.Model):
    id = models.AutoField(primary_key=True)#id random karışık olması için uuid tarzı ayarla
    first_user = models.ForeignKey(User, related_name="room_first", verbose_name="İlk Kullanıcı", on_delete=models.CASCADE)
    second_user = models.ForeignKey(User, related_name="room_second", verbose_name="İkinci Kullanıcı", on_delete=models.CASCADE)

class Message(models.Model):
    user = models.ForeignKey(User, related_name="messages", verbose_name="Kullanıcı", on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name="messages", verbose_name="Oda", on_delete=models.CASCADE)
    content = models.TextField(verbose_name="Mesaj İçeriği")
    created_at = models.DateTimeField(auto_now_add=True)

    def get_short_date(self):
        local_time = localtime(self.created_at)#django timezone kullanarak tarih ve saat bilgisini al
        return f"{local_time.hour}:{local_time.minute:02d}"
    
"""