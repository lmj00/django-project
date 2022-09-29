import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import Room, Message
from shop.models import Post


class ChatConsumer(AsyncWebsocketConsumer):
    
    @database_sync_to_async
    def save_message(self, room, user_id, post_id, message):
        Message.objects.create(
            roomname = room,
            content = message,
            post_id = post_id,
            user_id = user_id
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
        self.user = self.scope["user"]
        post_id = text_data_json['post_id']

        author_nickname = Post.objects.get(id=post_id).author.nickname
        room = Room.objects.get(id=text_data_json['room'])

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

        await self.save_message(room, self.user.id, post_id, message)

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
    
        nickname = ''

        if event['user_nickname'] == event['author_nickname']:
            nickname = event['author_nickname']
        else:
            nickname = event['user_nickname']

        message = nickname + ': ' + message
            
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
        }))

