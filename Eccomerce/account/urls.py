from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('register/' , UserRegisterView.as_view() , name='user_register'),
    path('verify/' , UserRegisterVerifyCodeView.as_view() , name='user_verify'),
    path('login/' , UserLoginView.as_view() , name='user_login'),
    path('logout/' , UserLogoutView.as_view() , name='user_logout'),
]