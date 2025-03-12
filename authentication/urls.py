
from django.contrib import admin
from django.urls import path
from .views import test,userRegister,verifyRegistration,loginUser,userDetail
urlpatterns = [
    path("",test.as_view()),
    path("register/",userRegister.as_view()),
    path("register/verify",verifyRegistration.as_view(),name='verify'),
    path("login/",loginUser.as_view(),name='login'),
    path("me/",userDetail.as_view(),name='userdetail'),
]
