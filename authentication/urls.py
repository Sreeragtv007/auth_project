
from django.urls import path
from .views import userRegister,verifyRegistration,loginUser,userDetail,logoutUser
urlpatterns = [
    path("register/",userRegister.as_view()),
    path("register/verify/",verifyRegistration.as_view(),name='verify'),
    path("login/",loginUser.as_view(),name='login'),
    path("me/",userDetail.as_view(),name='userdetail'),
    path("logout/",logoutUser.as_view(),name='logout'),
    
]
