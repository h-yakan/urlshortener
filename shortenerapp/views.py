from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Urls
# Create your views here.
def index(req):
    return render(req, 'base.html')

def saveUrl(req):
    Urls.objects.create(inUrl = req.POST["inUrl"], outSlug = req.POST["outSlug"])
    return render(req, 'success.html',
                  {'urls':Urls.objects.get(outSlug= req.POST["outSlug"])})

def shortenedRedirect(req,accessed_url):
    return HttpResponseRedirect(Urls.objects.get(outSlug = accessed_url).inUrl)