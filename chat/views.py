from django.shortcuts import render
from shop.models import Post
from chat.models import Room

# Create your views here.
def room(request, post_id, user_id): 
    
    post = Post.objects.get(id=post_id)
    check_buyer = len(Room.objects.filter(buyer_id=user_id))

    if check_buyer == 0:
        Room.objects.create(
            post_id = post_id, 
            seller_id = post.author.id, 
            buyer_id = user_id,
            last_content = ""
        )
    

    if post.author.id != user_id:
        room = Room.objects.get(post_id=post_id, buyer_id=user_id)


    return render(request, 'chat/room.html', {
        'post_id': post_id,
        'room': room.id
    })
