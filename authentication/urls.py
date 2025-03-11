
from django.contrib import admin
from django.urls import path
from .views import test,userRegister
urlpatterns = [
    path("",test.as_view()),
    path("register/",userRegister.as_view()),
]
