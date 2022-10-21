# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path(
        '<int:post_id>/<int:buyer_id>/', 
        views.room, 
        name='room'
    ),

    path(
        'room_list/', 
        views.RoomList.as_view(), 
        name='room_list'
    ),

    path(
        'polling/', 
        views.polling, 
        name='polling'
    ),

]