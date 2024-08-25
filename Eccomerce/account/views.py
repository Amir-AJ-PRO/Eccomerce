from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render , redirect
from django.views import View
from .forms import *
from utils import send_otp_code
import random
from django.contrib import messages
from .models import *
from django.contrib.auth import login , logout , authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime as d
from datetime import timedelta
from django.utils import timezone

class UserRegisterView(View):
    form_class = UserRegisterForm
    def get(self , request):
        form = self.form_class
        return render(request , 'account/register.html' , {'form' : form})

    def post(self , request):
        form = self.form_class(request.POST)
        if form.is_valid():
        
            if OtpCodeModel.objects.filter(phone_number=form.cleaned_data['phone']).exists() and timezone.now().minute <= OtpCodeModel.objects.get(phone_number=form.cleaned_data['phone']).created.minute + 1:
                messages.warning(request , 'We have sent you a code' , 'warning')
                return redirect('accounts:user_verify')
            else:
                if OtpCodeModel.objects.filter(phone_number=form.cleaned_data['phone']).exists():
                    OtpCodeModel.objects.get(phone_number=form.cleaned_data['phone']).delete()

                code = random.randint(1000,9999)
                print('=' * 90 , code)
                OtpCodeModel.objects.create(phone_number = form.cleaned_data['phone'] , otp=code)
                send_otp_code(phone=form.cleaned_data['phone'] , code=code)
                request.session['user_registration'] = {
                    'phone' : form.cleaned_data['phone'],
                    'full_name' : form.cleaned_data['full_name'],
                    'email' : form.cleaned_data['email'],
                    'password' : form.cleaned_data['password']
                }
                messages.success(request , 'we sent you a code' , 'success')
                return redirect('accounts:user_verify')
        return render(request , 'account/register.html' , {'form' : form})

class UserRegisterVerifyCodeView(View):
    forn_class = VerifyCodeForm
    def get(self , request):
        form = self.forn_class
        return render(request , 'account/verify.html' , {'form' : form})

    def post(self , request):
        user_session =  request.session['user_registration']
        code_instance = OtpCodeModel.objects.get(phone_number=user_session['phone'])
        form = self.forn_class(request.POST)

        if form.is_valid():
            start_date = timezone.now().date()
            end_date = start_date + timedelta( days=1 ) 
            time_code = OtpCodeModel.objects.get(phone_number=user_session['phone'] , created__range=(start_date, end_date))
            
            print(time_code.created)
            print(timezone.now())
            if form.cleaned_data['code'] == code_instance.otp :
                
                if timezone.now().minute > time_code.created.minute + 1 :
                    messages.error(request , 'This code was expired , try again' , 'danger')
                    code_instance.delete()
                    return redirect("accounts:user_verify")

                else:
                    User.objects.create_user(user_session['phone'] , user_session['email'] , user_session['full_name'] , user_session['password'])

                    code_instance.delete()
                    messages.success(request , 'You registered.' , 'success')
                    
                    user = authenticate(request , phone_number=user_session['phone'] , password=user_session['password'])
                    login(request , user)

                    return redirect("home:home")

            else:
                messages.error(request , 'Code is wrong' , 'danger')
                return redirect("accounts:user_verify")
            
        return render(request , 'account/verify.html' , {'form' : form})
    

class UserLoginView(View):
    form_class = LoginForm
    template_name = 'account/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self , request):
        form = self.form_class
        return render(request , self.template_name , {'form' : form})
    
    def post(self , request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = authenticate(request , phone_number=form.cleaned_data['phone_number'] , password=form.cleaned_data['password'])

            if user is not None:
                login(request , user)
                messages.success(request , 'Youre login is successfully' , 'success')
                return redirect('home:home')
            messages.error(request , 'phone or pass is incurrect' , 'danger')
        
        return render(request , self.template_name , {'form' : form})
    

class UserLogoutView(LoginRequiredMixin , View):

    def get(self , request):
        logout(request)
        messages.success(request , 'Youre log out is successfully' , 'success')
        return redirect('home:home')