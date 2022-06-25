from django.urls import reverse, reverse_lazy
from shop.forms import PostCreateForm, PostUpdateForm
from shop.models import Post
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView,
    DeleteView
)
from braces.views import LoginRequiredMixin, UserPassesTestMixin
from allauth.account.models import EmailAddress
from member.functions import confirmation_required_redirect

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


class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'shop/post_form.html'


    redirect_unauthenticated_users = True
    raise_exception = confirmation_required_redirect

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'post_id': self.object.id}) 
    
    def test_func(self, user):
        return EmailAddress.objects.filter(user=user, verified=True).exists()
		

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostUpdateForm
    template_name = 'shop/post_form.html'
    pk_url_kwarg = 'post_id'

    raise_exception = True

    def get_success_url(self):
        return reverse('post-detail', kwargs={'post_id': self.object.id}) 

    def test_func(self, user):
        return self.get_object().author == user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('posts')

    raise_exception = True

    def get_success_url(self):
        return reverse('posts')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def test_func(self, user):
        return self.get_object().author == user
