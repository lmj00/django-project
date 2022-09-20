from django.shortcuts import render
from shop.models import Post

# Create your views here.
def room(request, post_id):
    post = Post.objects.get(id__icontains=post_id)
    
    return render(request, 'chat/room.html', {
        'post_id': post_id,
        'post_author_id': post.author.id
    })
