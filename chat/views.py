from django.shortcuts import render
from shop.models import Post
from chat.models import Message, Room
from django.db.models import Q
from django.views.generic import ListView
from django.http import Http404
from django.http import JsonResponse


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


def polling(request):
    user_id = request.user.id

    check_room = Room.objects.filter( 
        Q(seller_id=user_id) | Q(buyer_id=user_id)
    )

    last_ms_list = request.GET.getlist('last_message[]')
    different_ms = []
    
    if len(check_room) > 0:
        for i in range(len(check_room)):
            message = Message.objects.filter(room_id=check_room[i].id) 
            
            if message.last().content != last_ms_list[i]:    
                different_ms.append(message.last().content)
            else:
                different_ms.append('')

        return JsonResponse(different_ms, safe=False)