from django import forms

from shortenerapp.models import Urls
from allauth.account.forms import SignupForm, AddEmailForm
from crispy_forms.layout import Layout, Field, Submit
from crispy_forms.helper import FormHelper
from django.contrib.auth.models import User,Group
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
#          super(MySignupForm, self).__init__(*args, **kwargs)
        
#     def save(self, request):
        
#          user = super(MySignupForm, self).save(request)
#          return user
    
# class MyEmailForm(AddEmailForm):
#     def __init__(self, *args, **kwargs):
#         super(MyEmailForm, self).__init__(*args, **kwargs)
#     first_name = forms.CharField(required=True)
#     last_name = forms.CharField(required=True)
#     user_group = forms.ModelChoiceField(queryset=Group.objects.all(),
#                                         widget=forms.RadioSelect,
#                                         initial=('particulier')
#                                         )
    
class MySignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(MySignupForm, self).__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs={"class":"d-none"}
        self.fields["password2"].widget.attrs={"class":"d-none"}
        self.fields["password1"].label=""
        self.fields["password2"].label=""
        self.fields["password1"].required=False
        self.fields["password2"].required=False
        self.fields["first_name"].label = "Adı"
        self.fields["last_name"].label = "Soyadı"

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    # _groups = forms.ModelChoiceField(queryset=Group.objects.all())
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    def save(self, request):
        
         user = super(MySignupForm, self).save(request)
         return user