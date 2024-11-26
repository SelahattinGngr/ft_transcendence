from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import json
from .models import Notification
from django.conf import settings
settings.configure()

class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name = 'notification_service'
        await self.channel_layer.group_add(
            self.group_name, 
            self.channel_name
        
        )
        await self.accept()
        await self.send(text_data=json.dumps({"message": "Connected"}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name, 
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            print("Mesaj alındı:", text_data_json)

            event = {
                'user_name': 'admin',
                'notification_type': 'notification_message',
                'content': message,
                'is_read': False,
            }
            print("Mesaj alındı2:", text_data_json)

            # Veritabanına bildirim kaydetme işlemi
            await self.save_notification(
                user_name=event['user_name'],
                notification_type=event['notification_type'],
                content=event['message'],
                is_read=event['is_read'],
            )
            print("Mesaj alındı3:", text_data_json)

            # Mesajı gruba gönder
            await self.channel_layer.group_send(self.group_name, event)
            print("Mesaj alındı4:", text_data_json)

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"message": "Invalid format. Must be JSON"}))

    # Veritabanı kaydetme işlemini asenkron hale getiren yardımcı fonksiyon
    @async_to_sync
    def save_notification(self, user_name, notification_type, content, is_read):
        Notification.objects.create(
            user_name=user_name,
            notification_type=notification_type,
            content=content,
            is_read=is_read,
        )

    # Bildirim alındığında çağrılır
    async def notification_message(self, event):

        await self.send(text_data=json.dumps({
            'user_name': event['user_name'],
            'notification_type': event['notification_type'],
            'content': event['message'],
            'is_read': event['is_read'],
        }))

