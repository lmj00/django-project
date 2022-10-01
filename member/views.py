from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import UpdateView, DetailView
from member.models import User, AddressCSV
from shop.models import Post
from member.forms import ProfileForm
from braces.views import LoginRequiredMixin
from allauth.account.views import PasswordChangeView

import json


# Create your views here.
class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    def get_success_url(self):
        return reverse('profile', kwargs={'user_id': self.request.user.id})


def popupAddress(request): 
    return render(request, 'member/popup_address.html') 


@csrf_exempt
@require_POST
def test(request):   
    jsonObject = json.loads(request.body)
    if jsonObject.get('sessionLatlng') is not None:
        request.session['lat'] = jsonObject.get('sessionLatlng').split(' ')[0]
        request.session['lon'] = jsonObject.get('sessionLatlng').split(' ')[1]
    else:
        return False


    if jsonObject.get('sessionAddr') is not None:
        addrData = AddressCSV.objects.get(name=jsonObject.get('sessionAddr'))

        if addrData is not None:
            request.session['addr'] = jsonObject.get('sessionAddr')
            return JsonResponse(jsonObject)

    return False

    
@csrf_exempt
@require_POST
def signupAddressCheck(request):
    if request.method == 'POST':
        jsonObject = json.loads(request.body)

        if request.session['lat'] is None or request.session['lon'] is None:
            return False

        if jsonObject.get('address') is not None:
            if jsonObject.get('address') == request.session['addr']:
                request.session['addr'] = jsonObject.get('address')
                return JsonResponse(jsonObject)

        return False    


class ProfileView(DetailView):
    model = User
    template_name = 'member/profile.html'
    pk_url_kwarg = 'user_id'
    context_object_name = 'profile_user'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
        query_set = Post.objects.filter(author__id=user_id).order_by("-dt_created")
        context['user_articles'] = query_set
        context['user_articles_count'] = len(query_set)
        
        return context


class ProfileSetView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'member/profile_set_form.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('index')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'member/profile_update_form.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('profile', kwargs=({'user_id': self.request.user.id}))