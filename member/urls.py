from django.urls import path
from . import views

urlpatterns = [ 
    path('popup_address/',  views.popupAddress, name='popup_address'),
    path('popup_address/test', views.test, name='test')
]