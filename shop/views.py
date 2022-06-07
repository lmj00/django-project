from shop.models import Post
from django.views.generic import ListView

# Create your views here.
class IndexView(ListView): 
    model = Post
    template_name = 'shop/index.html'
    context_object_name = 'posts'


class PostView(ListView):
    model = Post
    template_name = 'shop/post.html'
    context_object_name = 'posts'
    paginate_by: int = 8
    ordering = ['-dt_created']