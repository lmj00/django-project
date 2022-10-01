from django.urls import path
from . import views

urlpatterns = [ 
    path(
        'popup_address/',  
        views.popupAddress, 
        name='popup_address'
    ),
    path(
        'popup_address/test', 
        views.test, 
        name='test'
    ),
    path(
        'signup/addrCheck',
        views.signupAddressCheck, 
        name='address_check'
    ),
    path(
        'users/<int:user_id>/',
        views.ProfileView.as_view(),
        name='profile'
    ),
    path(
        'edit-profile/',
        views.ProfileSetView.as_view(),
        name='profile-set'
    ),
    path(
        'edit-profile/',
        views.ProfileUpdateView.as_view(),
        name='profile-update'
    )
]