from django.shortcuts import render
from django.urls import reverse
from allauth.account.views import PasswordChangeView

# Create your views here.
class CustomPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        return reverse('index')


def popupAddress(request):    
    return render(request, 'member/popup_address.html') 

