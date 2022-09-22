import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import Room, Message
from .models import User
from shop.models import Post

class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def save_message(self, user_id, post_id, message):
        post = Post.objects.get(id__icontains=post_id)

        check_user = len(Room.objects.filter(user_id=user_id))
        check_post = len(Room.objects.filter(post_id=post_id))

        if check_user > 0 and check_post > 0:
            test = Room.objects.get(user_id=user_id, post_id=post_id)
            print(test)
        else:
            if user_id != post.author.id:
                Room.objects.create(user_id=user_id, post_id=post_id, last_content="")

    #   Message.objects.create(
    #         seller=seller_id, buyer=buyer_id, content=message
    #     )


    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
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
        user_id = text_data_json['user_id']
        post_id = text_data_json['post_id']
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )    

        await self.save_message(user_id, post_id, message)

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
        }))

