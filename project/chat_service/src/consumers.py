import json

#from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    # web socketten servera bir mesaj geldiğinde
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = self.scope["user"]

        await self.save_to_database(message, user, self.room_name)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat.message", 
                "message": message,
                "user": user.username,
                "created_at": self.message_object.get_short_date()
                }
        )

    # serverdan clienta gönderirken
    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]
        created_at = event["created_at"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message, 
            "user": user,
            "created_at": created_at
        }))

    @database_sync_to_async
    def save_to_database(self, message, user, room):
        m=Message.objects.create(user=user, room_id=room, content=message)
        self.message_object=m