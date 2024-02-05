import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "MainRoom"
        self.room_group_name = "MainChat"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        username = self.scope['user'].username
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": json.dumps({
                'status': 'disconnect',
                'text': f'{username} вышел из чата!',
                'username': username
            })}
        )

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": text_data}
        )

    async def chat_message(self, event):
        message = event["message"]
        json_message = json.loads(message)

        if json_message['status'] != 'error':
            await self.send(message)

