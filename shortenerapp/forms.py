from django import forms

from shortenerapp.models import Urls
from allauth.account.forms import SignupForm
from django.contrib.auth.models import User,Group
from crispy_forms.helper import FormHelper
from allauth.account.forms import ResetPasswordForm,EmailAwarePasswordResetTokenGenerator
from allauth.account.utils import user_pk_to_url_str,user_username
from allauth.utils import build_absolute_uri
from allauth.account import app_settings
from allauth.account.app_settings import AuthenticationMethod
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from allauth.account.adapter import get_adapter


class URLGiris(forms.ModelForm):
    class Meta:
        model = Urls
        fields = ('inUrl','timer','isPublic')
        widgets = {'inUrl' : forms.TextInput(attrs={"class":"form-control"}),'isPublic': forms.CheckboxInput(), 'timer':forms.NumberInput(attrs={"class":"form-control"})}
        labels = {'inUrl':"Kısaltmak istediğiniz URL'yi girin",'timer':"Kısaltılmış URL'niz kaç günlük olsun",'isPublic':"Bu URL Herkese açık yapılsın mı? Cevabınız"}

class kisiSecim(forms.ModelForm):
    class Meta:
        model = Urls
        fields = ('allowedUsers',)
        labels = {'allowedUsers': "Kullanım izni vermek istediğiniz kişileri seçin"}
        widgets = {'allowedUsers': forms.SelectMultiple(attrs={"class":"form-control"})}

class MySignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(MySignupForm, self).__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs={"class":"d-none"}
        self.fields["password2"].widget.attrs={"class":"d-none"}
        self.fields["email"].widget.attrs={"class":"textinput form-control"}
        self.fields["first_name"].widget.attrs={"class":"textinput form-control"}
        self.fields["last_name"].widget.attrs={"class":"textinput form-control"}
        self.fields["groups"].widget.attrs={"class":"select2 select2-multiple"}
        self.fields["password1"].label=""
        self.fields["password2"].label=""
        self.fields["password1"].required=False
        self.fields["password2"].required=False
        self.fields["first_name"].label = "Adı"
        self.fields["last_name"].label = "Soyadı"
        self.fields["email"].required = True

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.SelectMultiple,
    )
    def clean_email(self):
        if not self.cleaned_data['email']:
           raise forms.ValidationError("Bir eposta girmek zorunludur") 
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu eposta zaten kullanılıyor")
        return email
    
    def save(self, request):
         user = super(MySignupForm, self).save(request)
         return user

default_token_generator = EmailAwarePasswordResetTokenGenerator()
class MyResetPasswordForm(ResetPasswordForm):
    def _send_password_reset_mail(self, request, email, users, **kwargs):
        token_generator = kwargs.get("token_generator", default_token_generator)

        for user in users:

            temp_key = token_generator.make_token(user)

            # save it to the password reset model
            # password_reset = PasswordReset(user=user, temp_key=temp_key)
            # password_reset.save()

            # send the password reset email
            uid = user_pk_to_url_str(user)
            path = reverse(
                "account_reset_password_from_key",
                kwargs=dict(uidb36=uid, key=temp_key),
            )
            url = build_absolute_uri(request, path)

            context = {
                "current_site": get_current_site(request),
                "user": user,
                "password_reset_url": url,
                "uid": uid,
                "key": temp_key,
                "request": request,
            }

            if app_settings.AUTHENTICATION_METHOD != AuthenticationMethod.EMAIL:
                context["username"] = user_username(user)
            get_adapter(request).send_mail(
                "emails/password_reset_key", email, context
            )                
