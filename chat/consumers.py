from datetime import datetime
import json
from time import time
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import Room, Message
from member.models import User
from shop.models import Post
from django.db.models import Q


class ChatConsumer(AsyncWebsocketConsumer):
    
    @database_sync_to_async
    def save_message(self, room, user, message):
        Message.objects.create(
            room = room,
            content = message,
            user = user
        )

        Room.objects.filter(id=room.id).update(last_content=message)

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()
    

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']   
        post_id = text_data_json['post_id']
        buyer_id = text_data_json['buyer_id']
        self.user = self.scope['user']

        post = Post.objects.get(id=post_id)
        buyer = User.objects.get(id=buyer_id)
        seller = User.objects.get(id=post.author.id)

        check_room = Room.objects.filter(
            Q(seller_id=post.author.id) & Q(buyer_id=buyer_id)
        )

        if len(check_room) == 0:
            Room.objects.create(
                post = post, 
                seller = seller,
                buyer = buyer,
                last_content = ""
        )

        room = Room.objects.get(
            Q(seller_id=post.author.id) & Q(buyer_id=buyer_id)
        )
        
        author_nickname = Post.objects.get(id=post_id).author.nickname

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_nickname': self.user.nickname,
                'author_nickname': author_nickname 
            }
        )    

        await self.save_message(room, self.user, message)


    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
        }))

