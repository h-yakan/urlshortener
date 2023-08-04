from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from shortenerapp.forms import URLGiris, kisiSecim
from .models import Urls
from django.utils.crypto import get_random_string
# Create your views here.

def success(req,slug):
    slug = slug

    return render(req, 'success.html', {'slug':slug,'host':req.META['HTTP_HOST']}
                  )
def form(req):
    def generateSlug():
        slug= get_random_string(8)
        slug_is_wrong = True  
        while slug_is_wrong:
            slug_is_wrong = False
            other_objs_with_slug = Urls.objects.filter(outSlug=slug)
            if len(other_objs_with_slug) > 0:
                slug_is_wrong = True
            if slug_is_wrong:
                slug = get_random_string(8)
        return slug
    

    if req.method == "POST":
    
        slug = generateSlug()
        form = URLGiris(req.POST)
        if form.is_valid():
            url = Urls(inUrl = form.cleaned_data['inUrl'],outSlug = slug,timer = form.cleaned_data['timer'],isPublic = form.cleaned_data['isPublic'])
            url.save()
            html = '/access/'+slug
            return redirect(html)
    else:
        form = URLGiris()
    return render(req, 'index.html',
                {'form':form})

def index(req):#burada kullanıcı girişi yoksa sadece url kısaltma formu çıkar. Tıklamak için giriş yap veya kaydol demesi gerekir. Eğer giriş yaptıysa iki tablo olarak kendisine ait kısa urller ve karşılıkları, bir de erişim izni olan urller ve karşılıkları bulunur. Sahip olduklarında paginator gibi objeleri sınırlayan bir şey olmalı ve objelerde sil butonu olmalı...
    if req.user.is_authenticated():
        ownedUrls = Urls.objects.filter(ownerUser__id = req.user.pk)
        return render(req,'index.html',{'ownedUrls':ownedUrls,})

@login_required
def erisimFormu(req,slug):
    url = get_object_or_404(Urls,outSlug = slug)
    if url.isPublic == 1:
        return render(req,'success.html',{'slug':slug,'host':req.META['HTTP_HOST']})
    else:
        if req.method == "POST":
            form = kisiSecim(req.POST, instance= url)
            form.save()
            return render(req,'success.html',{'slug':slug,'host':req.META['HTTP_HOST']})
        else:
            form = kisiSecim(instance = url)
            return render(req, "access.html",{'form':form})


@login_required
def shortenedRedirect(req,accessed_url):
    if Urls.objects.get(outSlug = accessed_url).isActive:
        return HttpResponseRedirect(Urls.objects.get(outSlug = accessed_url).inUrl)
    else:
        return HttpResponseBadRequest
    