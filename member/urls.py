from django.urls import path
from . import views

urlpatterns = [ 
    path(
        'popup-address/',  
        views.popupAddress, 
        name='popup-address'
    ),
    path(
        'popup-address/validator', 
        views.popupAddressValidator, 
        name='popup-validator'
    ),
    path(
        'address-validator',
        views.signupAddressValidator, 
        name='signup-address-validatror'
    ),
    path(
        '<int:user_id>/',
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