from django.shortcuts import render
from shop.models import Post
from chat.models import Message, Room
from django.db.models import Q
from django.views.generic import ListView

# Create your views here.
def room(request, post_id, user_id): 
    post = Post.objects.get(id=post_id)
    room = Room.objects.filter(buyer_id=user_id, seller_id=post.author.id)   

    # 채팅방 개설
    if len(room) == 0:
        Room.objects.create(
            post_id = post_id, 
            seller_id = post.author.id, 
            buyer_id = user_id,
            last_content = ""
        )
        
    room = Room.objects.get(
        Q(seller_id=post.author.id) & Q(buyer_id=user_id)
    )   

    message = Message.objects.filter(roomname_id=room.id)

    
    return render(request, 'chat/room.html', {
        'post_id': post_id, 
        'room': room.id, 
        'message_list': message 
    })



class RoomList(ListView):
    model = Room
    template_name = 'chat/room_list.html'    

    def get_queryset(self):
        user_id = self.request.user.id
        room = Room.objects.filter(
            Q(seller_id=user_id) | Q(buyer_id=user_id)
        )   

        return room
    