from datetime import timedelta
from random import randint
from django.forms import formset_factory
from django.utils import timezone
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from shortenerapp.forms import MyResetPasswordForm, MySignupForm, URLGiris, kisiSecim
from .models import SendMail, Urls
from django.utils.crypto import get_random_string
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailAddress
from django.conf import settings
from django.http import HttpRequest
from django.contrib.auth.models import User
# Create your views here.
def isAdmin(user):
    return user.is_superuser

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
            url = Urls(inUrl = form.cleaned_data['inUrl'],outSlug = slug,timer = form.cleaned_data['timer'],isPublic = form.cleaned_data['isPublic'],ownerUser = req.user)
            url.save()
            mailDate = url.expirationDate + timedelta(days = -1, minutes = 1)   
            mailToSend = SendMail(mail = req.user.email, mailtext = "Url'inizin süresi 1 gün sonra dolacak.", sendingDate = mailDate)
            mailToSend.save()
            # mailToSend.setup_task()
            html = '/access/'+slug
            return redirect(html)   
    else:
        form = URLGiris()
        if req.user.is_authenticated:
            ownedUrls = Urls.objects.filter(ownerUser__id = req.user.pk)
            return render(req, 'index.html',
                {'form':form,'ownedUrls':ownedUrls,'host':req.META['HTTP_HOST']})
        return render(req, 'index.html',
                {'form':form})


def index(req):
    if req.user.is_authenticated():
        ownedUrls = Urls.objects.filter(ownerUser__id = req.user.pk)
        return render(req,'index.html',{'ownedUrls':ownedUrls})
    else:
        pass

def deleteUrl(req,slug):
    url = Urls.objects.get(outSlug=slug)
    url.delete()
    return redirect('#')

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


@user_passes_test(isAdmin)
def userList(req):
    users = User.objects.all()
    if req.method == "POST":
        form = MySignupForm(req.POST)
        if form.is_valid():

            accAda= DefaultAccountAdapter()
            
            user =accAda.new_user(req)

            username = form.cleaned_data["email"].split("@")[0]
            while True:
                if User.objects.filter(username = username).exists():
                    username = username + str(randint(0,1000))
                else:
                    break
            form.cleaned_data['username'] = username
            # accAda.populate_username(request,user) username'yi isim soyisimden alır. Biz epostadan alıyoruz
            accAda.save_user(req,user,form)
            try:
                mail =EmailAddress.objects.get(email= user.email)
                mail.verified = 1
                mail.primary = 1
                mail.save()
            except:
                emailVerifier = EmailAddress.objects.create(email = user.email, verified = 1, primary = 1, user_id = user.pk)
                emailVerifier.save()
            selected_groups = form.cleaned_data["groups"]
            print(selected_groups)
            for group in selected_groups:
                user.groups.add(group)
                
            send_password_reset(user)
            form = MySignupForm()
            return render(req,'userList.html',{'users':users,'form':form})
        else:

            return render(req,'userList.html',{'form':form, 'users':users})
    else:
        form = MySignupForm()
        return render(req,'userList.html',{'form':form, 'users':users})

@login_required
def shortenedRedirect(req,accessed_url):
    if Urls.objects.get(outSlug = accessed_url).isActive :
        if Urls.objects.get(outSlug = accessed_url).isPublic:
            if Urls.objects.get(outSlug = accessed_url).expirationDate < timezone.now():
                url = Urls.objects.get(outSlug = accessed_url).isActive = False
                url.save()
                return HttpResponseBadRequest()
            else:
                return HttpResponseRedirect(Urls.objects.get(outSlug = accessed_url).inUrl)
        else:
            if Urls.objects.get(outSlug = accessed_url).allowedUsers.contains(req.user):
                if Urls.objects.get(outSlug = accessed_url).expirationDate < timezone.now():
                    url = Urls.objects.get(outSlug = accessed_url).isActive = False
                    url.save()
                    return HttpResponseBadRequest()
                else:
                    return HttpResponseRedirect(Urls.objects.get(outSlug = accessed_url).inUrl)
            else:
                return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()
    


def send_password_reset(user: settings.AUTH_USER_MODEL):
    request = HttpRequest()
    request.user = user
    request.META['HTTP_HOST'] = '127.0.0.1:8000'
    form = MyResetPasswordForm({"email": user.email})
    if form.is_valid():
        form.save(request)

@user_passes_test(isAdmin)
def addUsers(request):    
    if request.method == "POST":
        form = MySignupForm(request.POST)
        if form.is_valid():

            accAda= DefaultAccountAdapter()
            
            user =accAda.new_user(request)

            username = form.cleaned_data["email"].split("@")[0]
            while True:
                if User.objects.filter(username = username).exists():
                    username = username + str(randint(0,1000))
                else:
                    break
            form.cleaned_data['username'] = username
            # accAda.populate_username(request,user) username'yi isim soyisimden alır. Biz epostadan alıyoruz
            accAda.save_user(request,user,form)
            try:
                mail =EmailAddress.objects.get(email= user.email)
                mail.verified = 1
                mail.primary = 1
                mail.save()
            except:
                emailVerifier = EmailAddress.objects.create(email = user.email, verified = 1, primary = 1, user_id = user.pk)
                emailVerifier.save()
            selected_groups = form.cleaned_data["groups"]
            print(selected_groups)
            for group in selected_groups:
                user.groups.add(group)
                
            send_password_reset(user)
            return HttpResponse('Kayıt Başarılı')
        else:

            return render(request,'partials/_userForm.html',{'form':form})
    else:
        form = MySignupForm()

        return render(request,'addUsers.html',{'form':form})
        
def createUserForm(req):
    form = MySignupForm()
    return render(req,'partials/_userForm.html',{'form':form})


@user_passes_test(isAdmin)
def addUsersFormSet(request):    
    MySignupFormSet = formset_factory(form=MySignupForm,
    extra=1, can_delete=False, can_delete_extra=False
)
    if request.method == "POST":
        formset = MySignupFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    if form.cleaned_data:
                        accAda= DefaultAccountAdapter()
                
                        user =accAda.new_user(request)
                        username = form.cleaned_data["email"].split("@")[0]
                        while True:
                            if User.objects.filter(username = username).exists():
                                username = username + str(randint(0,1000))
                            else:
                                break
                        form.cleaned_data['username'] = username
                        
                        # else:
                            
                        #     accAda.populate_username(request,user) #username'yi isim soyisimden alır. Biz epostadan alıyoruz
                        accAda.save_user(request,user,form)
                        try:
                            mail =EmailAddress.objects.get(email= user.email)
                            mail.verified = 1
                            mail.primary = 1
                            mail.save()
                        except:
                            emailVerifier = EmailAddress.objects.create(email = user.email, verified = 1, primary = 1, user_id = user.pk)
                            emailVerifier.save()
                        selected_groups = form.cleaned_data["groups"]                    
                        for group in selected_groups:
                            user.groups.add(group)    
                        send_password_reset(user)
            formset = MySignupFormSet()
            return render(request,'signupTable.html',{'formset':formset, 'message':"Kayıt Başarılı"})
        else:

                    return render(request,'signupTable.html',{'formset':formset, 'message':"Kayıt başarısız oldu"})
    else:

        formset = MySignupFormSet()

        return render(request,'signupTable.html',{'formset':formset})