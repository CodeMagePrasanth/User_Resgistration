from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

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