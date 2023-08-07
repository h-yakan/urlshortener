from django import forms

from shortenerapp.models import Urls
from allauth.account.forms import SignupForm
from crispy_forms.layout import Layout, Field, Submit
from crispy_forms.helper import FormHelper

class URLGiris(forms.ModelForm):
    class Meta:
        model = Urls
        fields = ('inUrl','timer','isPublic')
        widgets = {'inUrl' : forms.TextInput(attrs={"class":"form-control"}),'isPublic': forms.CheckboxInput(), 'timer':forms.NumberInput(attrs={"class":"form-control"})}
        labels = {'inUrl':"Kısaltmak istediğiniz URL'yi girin",'timer':"Kısaltılmış URL'niz kaç günlük olsun",'isPublic':"Bu URL Herkese açık yapılsın mı? Cevabınız"}


# class kisiGiris(forms.ModelForm):
#     class Meta:
#         model = Urls
#         fields = ('isPublic',)
#         labels = {'isPublic':"Bu URL Herkese açık yapılsın mı? Cevabınız"}
#         widgets = {'isPublic': forms.Select(attrs={"class":"form-control"})}

class kisiSecim(forms.ModelForm):
    class Meta:
        model = Urls
        fields = ('allowedUsers',)
        labels = {'allowedUsers': "Kullanım izni vermek istediğiniz kişileri seçin"}
        widgets = {'allowedUsers': forms.SelectMultiple(attrs={"class":"form-control"})}


# class MySignupForm(SignupForm):
#     def __init__(self, *args, **kwargs):
#         super(MySignupForm, self).__init__(*args, **kwargs)
#         self.fields['first_name'] = forms.CharField(required=False)
#         self.fields['last_name'] = forms.CharField(required=False)
        
#     def save(self, request):
        
#         user = super(MySignupForm, self).save(request)
#         user.first_name = self.cleaned_data.pop('first_name')
#         user.last_name = self.cleaned_data.pop('last_name')
#         return user