from django.urls import reverse, reverse_lazy
from shop.forms import PostCreateForm, PostUpdateForm
from .models import Post, User
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
from django.shortcuts import render, redirect

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
    success_url = reverse_lazy('index')

    raise_exception = True

    def get_success_url(self):
        return reverse('index')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def test_func(self, user):
        return self.get_object().author == user


def distance(request, km):
    distance_list = []
    
    for j in Post.objects.values():
        start = float(request.user.lat), float(request.user.lon)
        goal = j['lat'], j['lon']
        distance = haversine(start, goal) 

        if km > distance: 
            distance_list.append(Post.objects.get(id=j['id'])) 

    return distance_list


def one_km(request):    
    posts = distance(request, 1)
    return render(request, 'shop/index.html', {'posts':posts})


def five_km(request):
    posts = distance(request, 5)
    return render(request, 'shop/index.html', {'posts':posts})


def ten_km(request):
    posts = distance(request, 10)
    return render(request, 'shop/index.html', {'posts':posts})


def all_km(request):
    context = {'posts': Post.objects.all()}
    return render(request, 'shop/index.html', context)


def permission_denied(request, exception): 
    response = render(request, "403.html", {})
    response.status_code = 403
    return response


def page_not_found(request, exception):
    response = render(request, "404.html", {})
    response.status_code = 404
    return response