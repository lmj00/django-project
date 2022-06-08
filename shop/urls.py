from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name = 'index'),
    path('posts', views.PostView.as_view(), name = 'posts'),
    path(
        'posts/<int:post_id>/',
        views.PostDetailView.as_view(), 
        name='post-detail'
    ),
]