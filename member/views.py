from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from allauth.account.views import PasswordChangeView
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
class CustomPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        return reverse('index')

def popupAddress(request): 
    return render(request, 'member/popup_address.html') 

@csrf_exempt
def test(request):   
    jsonObject = json.loads(request.body)
    # print(jsonObject)
    if jsonObject.get('session') is not None:
        request.session['lat'] = jsonObject.get('session').split(' ')[0]
        request.session['lon'] = jsonObject.get('session').split(' ')[1]
        # request.session['lat'] = None
        # request.session['lon'] = None
    
    return JsonResponse(jsonObject)