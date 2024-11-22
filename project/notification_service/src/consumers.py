from channels.generic.websocket import AsyncWebsocketConsumer
import json
#from project.notification_service import notification_service

class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name = 'notification_service'
        # Kullanıcıyı gruba ekle
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        # Bağlantıyı kabul et
        await self.accept()
        await self.send(text_data=json.dumps({"message" : "Connected"}))

    async def disconnect(self, close_code):
        # Kullanıcıyı gruptan çıkar
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']

            event = {
                'type': 'notification_message',
                'message': message
            }

            await self.channel_layer.group_send(self.group_name, event)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"message" : "Invalid format. Must be JSON"}))
        #gruptaki herkese mesajı gönderir

    # Bildirim alındığında çağrılır
    async def notification_message(self, event):
        # Mesajı kullanıcıya gönder
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message'],
        }))
        #olayları websocket istemcisine iletir
