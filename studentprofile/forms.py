from django import forms
from studentprofile.models import profile, UserProfile
from django.contrib.auth.models import User

class profileform(forms.ModelForm):
    class Meta:
        model = profile
        fields = ('github','codecademy','teamtreehouse','codewars')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)