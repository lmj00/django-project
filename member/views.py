from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from allauth.account.views import PasswordChangeView
from django.views.decorators.csrf import csrf_exempt
from .models import AddressCSV
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
    if jsonObject.get('sessionLatlng') is not None:
        request.session['lat'] = jsonObject.get('sessionLatlng').split(' ')[0]
        request.session['lon'] = jsonObject.get('sessionLatlng').split(' ')[1]
    else:
        # return messages.info(request, "테스트")
        # messages.error(request, '위도 경도 없음')
        return False

    if jsonObject.get('sessionAddr') is not None:
        # print(jsonObject.get('sessionAddr'))
        addrData = AddressCSV.objects.get(name=jsonObject.get('sessionAddr'))

        # print(addrData)
        if addrData is not None:
            request.session['addr'] = jsonObject.get('sessionAddr')
        else:
            return False

            # messages.error(request, '주소 없음')
    else:
        return False
        # messages.error(request, '주소 없음')


    return JsonResponse(jsonObject)


@csrf_exempt
def signupAddressCheck(request):
    jsonObject = json.loads(request.body)

    if request.session['lat'] is None or request.session['lon'] is None:
        return False

    if jsonObject.get('address') is not None:
        if jsonObject.get('address') == request.session['addr']:
            request.session['addr'] = jsonObject.get('address')
        else:
            return False
    else:
        return False


    return JsonResponse(jsonObject)
