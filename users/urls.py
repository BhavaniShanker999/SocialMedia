
from django.urls import path,include
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('create_user/',CreateUser.as_view()),
    path('login_user/',Login.as_view()),
    path('logout_user/',Logoutview.as_view()),
    path('changepassword/',ChangePassword.as_view()),
    ]
