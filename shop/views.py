from django.shortcuts import redirect
from django.urls import reverse
from shop.forms import PostCreateForm, PostUpdateForm
from shop.models import Post
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView,
)
from braces.views import LoginRequiredMixin

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


class PostDetailView(DetailView):
    model = Post
    template_name = 'shop/post_detail.html'
    pk_url_kwarg = 'post_id'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'shop/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'post_id': self.object.id}) 


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostUpdateForm
    template_name = 'shop/post_form.html'
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse('post-detail', kwargs={'post_id': self.object.id}) 


def PostDelete(request, post_id):
    Post.objects.get(id=post_id).delete()

    return redirect('posts') 