from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from shortenerapp.forms import URLGiris
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
            url = Urls(inUrl = form.cleaned_data['inUrl'],outSlug = slug)
            url.save()
            html = '/success/'+slug
            return redirect(html)
    else:
        form = URLGiris()
    return render(req, 'index.html',
                {'form':form})
# def saveUrl(req):
#     def generateSlug():
#         slug= get_random_string(8)
#         slug_is_wrong = True  
#         while slug_is_wrong:
#             slug_is_wrong = False
#             other_objs_with_slug = Urls.objects.filter(outSlug=slug)
#             if len(other_objs_with_slug) > 0:
#                 slug_is_wrong = True
#             if slug_is_wrong:
#                 slug = get_random_string(8)
#         return slug
    
#     slug = generateSlug()
#     form = URLGiris(req.POST)
#     if form.is_valid:
#         url = Urls(inUrl = form["inUrl"],outSlug = slug)
#         url.save()
#         return render(req, 'success.html',
#                   {'urls':url,'form':form})
    

def shortenedRedirect(req,accessed_url):
    return HttpResponseRedirect(Urls.objects.get(outSlug = accessed_url).inUrl)