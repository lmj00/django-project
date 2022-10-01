from django import forms
from .models import User

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['address']


    def signup(self, request, user):
        # user.nickname = self.cleaned_data['nickname']
        user.address = request.session['addr']
        user.lat = float(request.session['lat'])
        user.lon = float(request.session['lon'])
        user.save()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'nickname',
            'profile_pic'
        ]