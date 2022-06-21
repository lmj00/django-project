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
    path(
        'posts/new/', 
        views.PostCreateView.as_view(),
        name='post-create'
    ),
    path(
        'posts/<int:post_id>/edit/',
        views.PostUpdateView.as_view(),
        name='post-update'
    ),
    path(
        'posts/<int:post_id>/delete/',
        views.PostDelete,
        name='post-delete'
    ),
]