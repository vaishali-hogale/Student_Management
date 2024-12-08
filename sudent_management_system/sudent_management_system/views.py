import django.shortcuts
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from app.EmailBackEnd import EmailBackEnd
from app.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,HttpResponse


def BASE(request):
    return django.shortcuts.render(request, 'base.html'),


def LOGIN(request):
    return django.shortcuts.render(request, 'login.html')


def doLogin(request):
    if request.method=="POST":
        user = EmailBackEnd.authenticate(request,
                                       username=request.POST.get('email'),
                                       password=request.POST.get('password'),)

        if user!=None:
            login(request,user)
            user_type = user.user_type
            if user_type=='1':
                return redirect('hod_home')
            elif user_type=='2':
                return redirect('staff_home')

            elif user_type=='3':
                return HttpResponse('This is Student Panel')

            else:
                messages.error(request, 'Invalid Email or Password')
                return redirect('login')

        else:
            messages.error(request, 'Invalid email or password')
            return  redirect('login')

def doLogout(request):
    logout(request)
    return django.shortcuts.redirect('login')

@login_required(login_url='/')

def PROFILE(request):
    user = CustomUser.objects.get(id=request.user.id)
    context={
        "user":user,
    }
    return render(request,'profile.html',context)

@login_required(login_url='/')

def PROFILE_UPDATE(request):

    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        # email=request.POST.get('email')
        # username=request.POST.get('username')
        password = request.POST.get('password')
        print(profile_pic)
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name = last_name

            if password != None and password != "":
                customuser.set_password(password)
            if profile_pic != None and profile_pic != "":
                customuser.profile_pic = profile_pic

            customuser.save()
            messages.success(request, "Profile update Successfully!")
            return redirect('profile')


        except:
            messages.error(request, "Failed!")


    return render(request, 'Profile.html')
