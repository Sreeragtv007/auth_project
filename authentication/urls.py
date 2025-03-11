
from django.contrib import admin
from django.urls import path
from .views import test,userRegister,verifyRegistration
urlpatterns = [
    path("",test.as_view()),
    path("register/",userRegister.as_view()),
    path("register/verify",verifyRegistration.as_view(),name='verify'),
]
