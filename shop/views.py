from shop.models import Post
from django.views.generic import ListView

# Create your views here.
class IndexView(ListView): 
    model = Post
    template_name = 'shop/index.html'
    context_object_name = 'posts'