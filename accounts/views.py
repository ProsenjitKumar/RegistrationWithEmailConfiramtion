from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import Reg
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from .token import activation_token

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return render(request, 'thankyou.html')
        else:
            return HttpResponse("Username or password incorrect")
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')

def home(request):
   return render(request, 'home.html')


def user_signup(request):
    form = Reg(request.POST or None)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.is_active = False
        instance.save()
        site=get_current_site(request)
        mail_subject='Confarmation messag for blog'
        message=render_to_string('confarm_email.html',{
            "user":instance,
            'domain':site.domain,
            'uid':instance.id,
            'token':activation_token.make_token(instance)
        })
        to_email=form.cleaned_data.get('email')
        from_email=settings.EMAIL_HOST_USER
        send_mail(mail_subject,message,from_email,[to_email],fail_silently=False)

        return HttpResponse("<h1>Thanks for your Registration A confarmation link was send your email</h1>")

    return render(request, 'signup.html',{'signup_form':form})

def activate(request):
    return render_to_string()