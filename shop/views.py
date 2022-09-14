from django.urls import reverse, reverse_lazy
from shop.forms import PostCreateForm, PostUpdateForm
from shop.models import Post, User
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
from django.db.models import Q
from haversine import haversine

# Create your views here.
class IndexView(ListView): 
    model = Post
    template_name = 'shop/index.html'
    context_object_name = 'posts'
    paginate_by: int = 8

    def get_queryset(self):
        return Post.objects.filter(is_sold=False).order_by('-dt_created')


class PostSearchView(ListView):
    model = Post
    template_name = 'shop/post_search.html'
    paginate_by: int = 8
    ordering = ['-dt_created']

    def get_queryset(self):
        search = self.request.GET.get('searched')
        check = Post.objects.filter(           
            Q(title__icontains=search) | Q(address__icontains=search)
        )    
        return check

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['searched'] = self.request.GET.get('searched')
        return context
    

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
        form.instance.address = self.request.user.address
        form.instance.lat = self.request.user.lat
        form.instance.lon = self.request.user.lon
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


class PostDistanceView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'shop/post_distance.html'

    def get_queryset(self):
        bar = self.request.GET.get('bar')
        start = float(self.request.user.lat), float(self.request.user.lon)
        value = Post.objects.values()
        distance_list = []

        for i in value:
            goal = i['lat'], i['lon']
            distance = haversine(start, goal) 

            if int(bar) > distance:
                distance_list.append(Post.objects.get(id=i['id'])) 
        
        return distance_list


class ProfileView(DetailView):
    model = User
    template_name = 'shop/profile.html'
    pk_url_kwarg = 'user_id'
    context_object_name = 'profile_user'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
        context['user_articles'] = Post.objects.filter(author__id=user_id).order_by("-dt_created")
        return context