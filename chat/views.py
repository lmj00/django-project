from django.shortcuts import render
from shop.models import Post
from chat.models import Message, Room
from django.db.models import Q
from django.views.generic import ListView
from django.http import Http404

# Create your views here.
def room(request, post_id, buyer_id): 
    post = Post.objects.get(id=post_id)
    user_id = request.user.id

    if request.user.id != buyer_id and request.user.id != post.author.id:
        raise Http404

    room_list = Room.objects.filter(
        Q(seller_id=user_id) | Q(buyer_id=user_id)
    )   

    check_room = Room.objects.filter(
        Q(seller_id=post.author.id) & Q(buyer_id=buyer_id)
    )

    if len(check_room) > 0:
        room = Room.objects.get(
            Q(seller_id=post.author.id) & Q(buyer_id=buyer_id)
        )
        message = Message.objects.filter(room=room.id)
    else:
        message = ""

    return render(request, 'chat/room.html', {
        'post_id': post_id, 
        'buyer_id': buyer_id,
        'message_list': message,
        'room_list': room_list
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