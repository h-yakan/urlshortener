from django import forms

from shortenerapp.models import Urls

class URLGiris(forms.ModelForm):
    class Meta:
        model = Urls
        fields = ('inUrl',)
        labels = {'inUrl':"Kısaltmak istediğiniz URL'yi girin"}
        widgets = {'inUrl' : forms.TextInput(attrs={"class":"form-control"}),}

