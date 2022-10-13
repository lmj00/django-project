# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path(
        '<int:post_id>/<int:user_id>/', 
        views.room, 
        name='room'
    ),
]