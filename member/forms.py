from django import forms
from .models import User

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'address']
    

    def signup(self, request, user):
        user.nickname = self.cleaned_data['nickname']
        user.address = self.cleaned_data['address']
        user.lat = float(request.session['lat'])
        user.lon = float(request.session['lon'])
        user.save()