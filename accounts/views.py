from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import authenticate , login
from .forms import SignUpForm,LoginUserForm,ChangePasswordForm,ProfileForm1,ProfileForm2
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserProfile



# Create your views here.
########User Login################
def login(request):
    if request.method == 'POST':
        fm=LoginUserForm(request.POST)
        
        if fm.is_valid():
            email = fm.cleaned_data['username']
            password = fm.cleaned_data['password']
            user = None
            user = User.objects.get(email = email)
            result = auth.authenticate(username = user.username , password = password)             
            if(result is not None):
                auth.login(request,result)
                next_page = request.GET.get('next')
                if next_page is not None:
                    messages.success(request,'Login Successfully')
                    return redirect(next_page)
                else:
                    messages.success(request,'Login Successfully')
                    return redirect('home')
            else:
                messages.error(request,'Invalid Credentials')
                fm=LoginUserForm(request.POST)
                context={
                    'form':fm,
                }
                return render(request,'accounts/login.html',context)
            
        else:
            fm=LoginUserForm(request.POST)
            context={
                'form':fm,
            }
            return render(request,'accounts/login.html',context)
    fm=LoginUserForm()
    context={
        'form':fm,
    }
    return render(request,'accounts/login.html',context)


########User Register################
def signup(request):
    if request.method == 'POST':
        fm=SignUpForm(request.POST)
        if fm.is_valid():
            user=fm.save()            
            ########### Create a user profile##########Immediate after creating user creating user's profile & mapp user with profile
            profile = UserProfile()
            profile.user = user
            profile.profile_picture = 'default.jpg'
            profile.save()
            messages.success(request,'You are Now Successfully Registered')
            return redirect('login')
            
        else:
            fm=SignUpForm(request.POST)
            context={
                'form':fm,
            }
            return render(request,'accounts/signup.html',context)
    
    fm=SignUpForm()
    context={
        'form':fm,
    }
    return render(request,'accounts/signup.html',context)


##############Logout user & Redirected to home page#################
@login_required(login_url='login')   
def user_logout(request):
    auth.logout(request)
    messages.success(request,'You are Now Successfully Logged Out')
    return redirect('home')


###########Changing user password#############
################change user password from Loggedin user############
@login_required(login_url='login')
def changeuserpassword(request):
    if request.method =='POST':
        fm=ChangePasswordForm(user=request.user,data=request.POST)
        if fm.is_valid():
            fm.save()        
            messages.success(request,'Your Password Is Changed Successfully')
            return redirect('login')
        else:
            context={
                'form':fm
            }
            fm=ChangePasswordForm(user=request.user,data=request.POST)
            return render(request,'accounts/changepassword.html',context)
    else:
        fm=ChangePasswordForm(user=request.user)
        context={
            'form':fm
        }
        return render(request,'accounts/changepassword.html',context)

###############User Profile#################
@login_required(login_url='login')   
def UpdateProfile(request):
    query_set = UserProfile.objects.get(user_id=request.user.id)  ####This will return user profile with mathcing user.id###########
    profile_dp=query_set.profile_picture############This will retreive profile_picture of user profile model
    # if not profile_dp:
    #     profile_dp='media/default.jpg'
    user_updated_date=query_set.updated_date#######This will retreive user_updated_date of user profile model
    if request.method =='POST':
       
        
        fm1=ProfileForm1(request.POST,instance=request.user)
        fm2=ProfileForm2(request.POST,request.FILES,instance=query_set)
        if fm1.is_valid() and fm2.is_valid():
            fm1.save()
            fm2.save()
            messages.success(request,'Your Profile Is Successfully Saved')
            return redirect('UpdateProfile')
        else:
            fm1=ProfileForm1(request.POST,instance=request.user)
            fm2=ProfileForm2(request.POST,request.FILES,instance=query_set)
            context={
                'form1':fm1,
                'form2':fm2,
            }
            
            return render(request,'accounts/profile.html',context)

    else:
        fm1=ProfileForm1(instance=request.user)
        fm2=ProfileForm2(instance=query_set)
        context={
            'form1':fm1,
            'form2':fm2,
            ############Some additional information of ProfileModel related to specific user
            'profile_picture':profile_dp,
            'updated_time':user_updated_date,
        }
        return render(request,'accounts/profile.html',context)