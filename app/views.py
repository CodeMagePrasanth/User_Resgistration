from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect

from app.forms import *

from django.core.mail import send_mail

from django.contrib.auth import authenticate,login,logout

from django.urls import reverse

from django.contrib.auth.decorators import login_required
 
def registration(request):
    USFO=UserForm()
    PFO=ProfileForm()
    d={'USFO':USFO,'PFO':PFO}

    if request.method=='POST' and request.FILES:
        UFDO=UserForm(request.POST)
        PFDO=ProfileForm(request.POST,request.FILES)

        if UFDO.is_valid() and PFDO.is_valid():
            MUFDO=UFDO.save(commit=False)
            MUFDO.set_password(UFDO.cleaned_data['password'])
            MUFDO.save()

            MPFDO=PFDO.save(commit=False)
            MPFDO.username=MUFDO
            MPFDO.save()

            send_mail('Welcome to IT world',
                      'Join our Team, Imporve your connection',
                      'prasanthsenthilkumaran@gmail.com',
                      [MUFDO.email],
                      fail_silently=False
                      )
            
            return HttpResponse('Registration is successfull')

    return render(request,'registration.html',d)

def dummy(request):
    return render(request,'dummy.html')

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)

    return render(request,'home.html')

def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        user=authenticate(username=username,password=password)

        if user and user.is_active:
            login(request,user)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('u r not an authenticated user')
    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def profile_display(request):
    un=request.session.get('username')
    UO=User.objects.get(username=un)
    PO=Profile.objects.get(profile_user=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'profile_display.html',d)

@login_required
def change_password(request):

    if request.method=='POST':
        pw=request.POST['password']

        un=request.session.get('username')
        UO=User.objects.get(username=un)

        UO.set_password(pw)
        UO.save()
        return HttpResponse('password is changed successfully')

    return render(request,'change_password.html')


def reset_password(request):

    if request.method=='POST':
        un=request.POST['un']
        pw=request.POST['pw']

        LUO=User.objects.filter(username=un)

        if LUO:
            UO=LUO[0]
            UO.set_password(pw)
            UO.save()
            return HttpResponse('password reset is done')
        else:
            return HttpResponse('user is not present in my DB')
        

        return HttpResponse('Reset password is done successfully')
    return render(request,'reset_password.html')