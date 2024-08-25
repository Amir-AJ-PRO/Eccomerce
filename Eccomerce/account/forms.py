from typing import Any
from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

class UserCreateinfoForm(forms.ModelForm):
    password1 = forms.CharField(label='password' , widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password' , widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email' , 'phone_number' , 'full_name')

    def clean_password2(self):
        cd = self.cleaned_data

        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('password must match')

    def save(self, commit=True):

        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        
        if commit:
            user.save()
        return user
        
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="you cant change password using <a href=\"../password/\"> this form </a>")
    class Meta:
        model = User 
        fields = ('email' , 'phone_number' , 'full_name' , 'password' , 'last_login')

class UserRegisterForm(forms.Form):
    phone = forms.CharField(max_length=11)
    full_name = forms.CharField(label='full name')
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    #def claen_phone(self):
    #    phone = self.cleaned_data['phone']
    #    if User.objects.filter(phone_number=phone).exists() :
    #        raise ValidationError('This phone is already used')
    #    return phone
#
    #def claen_email(self):
    #    email = self.cleaned_data['email']
    #    user = User.objects.filter(email=email).exists()
#
    #    if user :
    #        raise ValidationError('This email is already used')
#
    #    return email
    
    def clean(self):
        cd = super().clean()

        # insted clean_data function ... :

        email = cd.get('email')
        euser = User.objects.filter(email=email).exists()
        if euser :
            raise ValidationError('This email is already used')
        
        phone = self.cleaned_data['phone']
        if User.objects.filter(phone_number=phone).exists() :
            raise ValidationError('This phone is already used')
        

class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()


class LoginForm(forms.Form):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}))    