import json
from channels.generic.websocket import AsyncWebsocketConsumer


class CallConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for WebRTC call signaling using a shared room.
    Supports exactly two users per room.
    """

    async def connect(self):
        self.user = self.scope["url_route"]["kwargs"]["username"]
        self.room_name = f"call_{self.scope['url_route']['kwargs']['room_name']}"

        # Join the room
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name,
        )

        await self.accept()

        # Notify room that a user joined
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "user_joined",
                "user": self.user,
            },
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name,
        )

        # Notify room that a user left
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "user_left",
                "user": self.user,
            },
        )

    async def receive(self, text_data):
        """
        Handles WebRTC signaling messages:
        - offer
        - answer
        - ice-candidate
        """
        data = json.loads(text_data)
        message_type = data["type"]

        # Broadcast signaling message to the room
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "signal_message",
                "signal_type": message_type,
                "user": self.user,
                "data": data.get("data"),
            },
        )

    async def signal_message(self, event):
        """
        Send signaling data to WebSocket clients.
        Sender also receives it (frontend can ignore self messages).
        """
        await self.send(
            text_data=json.dumps(
                {
                    "type": event["signal_type"],
                    "user": event["user"],
                    "data": event["data"],
                }
            )
        )

    async def user_joined(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "user_joined",
                    "user": event["user"],
                }
            )
        )

    async def user_left(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "user_left",
                    "user": event["user"],
                }
            )
        )
