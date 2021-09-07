from django import forms
from django.http import request
from django.contrib.auth.models import User
from django.contrib import auth
from django.forms import ValidationError
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from .models import UserProfile
from .choices import CITY_CHOICES




# Sign Up Form from django UserCreationForm
class SignUpForm(UserCreationForm):
   
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Your First Name'}),max_length=50, required=False, help_text='(Optional)')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Your Last Name'}),max_length=50, required=False, help_text='(Optional)')
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Your Username'}),max_length=50)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Your Email'}),max_length=100)
    password1= forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Your Password'}),label='Password',min_length=5,max_length=40)
    password2= forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}),label='Confirm Password',max_length=40)
    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name',
            'username',
            'email', 
            'password1',
            'password2',
            ]
############function to validate if email is already in database defclean_fieldname method to raise custom validation##############
    def clean_email(self):
        email = self.cleaned_data['email']
        obj = User.objects.filter(email=email)#####To check if user with email Already in database####
        if obj:
            raise forms.ValidationError('Email Already Exists.Try With New Email')
        else:
            return email
#####################################################Login Form####################
            
class LoginUserForm(forms.ModelForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Your Email'}),max_length=100,help_text='Please Enter a Valid Email',label='Email Address')
    password= forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Your Password'}),label='Password',min_length=3,max_length=50)
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]
################Change password form##########
        
class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model=User

#############UserEdit profile-form1###########Showing 3 fields from Account Model
class ProfileForm1(forms.ModelForm):
    first_name= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'(Optional)'}),max_length=30,required=False)
    last_name= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'(Optional)'}),max_length=30,required=False)
    
    class Meta:
        model=User
        fields = [
            'first_name', 
            'last_name', 
            
        ]
            
#############UserEdit profile-form2###########Showing All fields from Userprofile Model
class ProfileForm2(forms.ModelForm):
    address_line_1= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'(Optional)'}),max_length=100,required=False)
    address_line_2= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'(Optional)'}),max_length=50,required=False)
    city= forms.CharField(widget=forms.Select(choices=CITY_CHOICES,attrs={'placeholder':'(Optional)'}),max_length=30,required=False)
    class Meta:
        model=UserProfile
        fields = '__all__'
        exclude=['user']