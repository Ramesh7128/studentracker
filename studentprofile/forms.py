from django import forms
from studentprofile.models import profile

class profileform(forms.ModelForm):
    class Meta:
        model = profile
        fields = ('github','codecademy','teamtreehouse','codewars')
        fields = ('github','codecademy','teamtreehouse','codewars')