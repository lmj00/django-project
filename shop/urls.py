from django.urls import path
from . import views
from django.conf.urls import (
    handler403, handler404
)

handler403 = 'shop.views.permission_denied'
handler404 = 'shop.views.page_not_found'

urlpatterns = [
    path('', views.IndexView.as_view(), name = 'index'),
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
        views.PostDeleteView.as_view(),
        name='post-delete'
    ),
    path(
        'posts/search/',
        views.PostSearchView.as_view(),
        name='post-search'
    ),
    
    # distance
    path(
        'one/',
        views.one_km, 
        name='one_km'
    ),
    path(
        'five/',
        views.five_km, 
        name='five_km'
    ),
    path(
        'ten/',
        views.ten_km, 
        name='ten_km'
    ),
    path(
        'all/',
        views.all_km, 
        name='all_km'
    ),

]