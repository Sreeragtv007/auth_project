from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Userotp

from authentication.utilis import generateOtp, sendMail
# Create your views here.


class test(APIView):
    def get(self, request):
        return HttpResponse("Hello World")


class userRegister(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if User.objects.filter(email=email).exists():
            return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

        otp = generateOtp()
        message = f"Your OTP is {otp}"
        subject = "OTP for Registration"
        mail = sendMail(email, otp, message, subject)
        if mail == True:
            if Userotp.objects.filter(email=email).exists():
                Userotp.objects.filter(email=email).update(otp=otp)
            else:
                Userotp.objects.create(email=email, otp=otp)
        else:
            return Response({'error': 'unexpexted error found'}, status=status.HTTP_400_BAD_REQUEST)

        return Response("User Registered", status=status.HTTP_201_CREATED)
