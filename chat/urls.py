# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('<str:post_id>/', views.room, name='room'),
]