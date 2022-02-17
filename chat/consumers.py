from channels.generic.websocket import AsyncWebsocketConsumer
import json
from datetime import datetime 
from channels.db import database_sync_to_async
from .models import Message
from dateutil.parser import parse

class chatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    
    @database_sync_to_async
    def update_messages_db(self, username, dateTime, message):
        newMsg = Message.objects.create(sent_by=username, sent_on=parse(dateTime), msg= message, sent_to_room=self.room_name)
        newMsg.save()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        dateTime = text_data_json["dateTime"]

        await self.update_messages_db(username, dateTime, message)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
                'username':username,
                'dateTime': dateTime
            }
        )

    async def chatroom_message(self, event):
        message = event["message"]
        username = event["username"]
        dateTime = event["dateTime"]

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'dateTime': dateTime
        }))
