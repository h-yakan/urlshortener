from django import forms

from shortenerapp.models import Urls

class URLGiris(forms.ModelForm):
    class Meta:
        model = Urls
        fields = ('inUrl','timer','isPublic')
        labels = {'inUrl':"Kısaltmak istediğiniz URL'yi girin",'timer':"Kısaltılmış URL'niz kaç günlük olsun",'isPublic':"Bu URL Herkese açık yapılsın mı? Cevabınız"}
        widgets = {'inUrl' : forms.TextInput(attrs={"class":"form-control"}),'isPublic': forms.CheckboxInput()}

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
