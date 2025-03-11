from django.shortcuts import redirect, render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Userotp
from .serializers import UserotpSerializer
from authentication.utilis import generateOtp, sendMail
# Create your views here.


class test(APIView):
    def get(self, request):
        return HttpResponse("Hello World")


class userRegister(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        otp = generateOtp()
        request.data['otp'] = otp

        if User.objects.filter(email=email).exists():
            return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

        

        subject = f"Your OTP is {otp}"
        message = "OTP for Registration"
        mail = sendMail(email, otp, message, subject)
        if mail == True:
            if Userotp.objects.filter(email=email).exists():
                Userotp.objects.filter(email=email).update(otp=otp)
            else:
                serializer = UserotpSerializer(data=request.data)
                
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'unexpexted error found'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'OTP sent to your email'}, status=status.HTTP_200_OK)


class verifyRegistration(APIView):
    def post(self, request):
        
        email = request.data.get('email')
        otp = request.data.get('otp')

        if Userotp.objects.filter(email=email, otp=otp).exists():
            userotp=Userotp.objects.filter(email=email, otp=otp)
            print(userotp)
            user = User.objects.create_user(email=email, username=email)
            userotp.delete()
            
            return Response({'message': 'User Verified and account created'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
