from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import Userotp
from .serializers import UserotpSerializer, userSerilaizer
from authentication.utilis import generateOtp, sendMail
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.authtoken.models import Token
# Create your views here.


class test(APIView):
    def get(self, request):
        return HttpResponse("Hello World")


class userRegister(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        otp = generateOtp()
        data['otp'] = otp

        subject = f"Your OTP is {otp}"
        message = "OTP for Registration"

        userotp = Userotp.objects.filter(email=data['email'])
        if userotp:
            userotp.update(otp=otp)
        else:
            serializer = UserotpSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors)
        mail = sendMail(data['email'], otp, message, subject)
        if mail == True:

            return Response({'message': "otp sent to emial"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "unexpexted error found while sending otp"}, status=status.HTTP_400_BAD_REQUEST)


class verifyRegistration(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        try:
            otp_obj = Userotp.objects.get(email=data['email'], otp=data['otp'])
        except:
            return Response({"message": "otp or email enterd invalid "})

        if otp_obj:
            request.data['password'] = otp_obj.password
            request.data['username'] = otp_obj.email
            serializer = userSerilaizer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                otp_obj.delete()
                return Response({"message": "otp validated and user created"},status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors)
        else:
            return Response({"message": "otp or email enterd invalid "}, status=status.HTTP_400_BAD_REQUEST)

     


class loginUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(username=email, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            response = Response({'message': 'Login successful'})
            response.set_cookie(
                key='auth_token',
                value=token.key,
                # Prevents JavaScript access (XSS protection)
                httponly=True,
                samesite='Lax',  # Adjust based on frontend/backend deployment setup
                secure=True  # Use only in HTTPS environments
            )
            return response
        return Response({'error': 'Invalid credentials'}, status=400)


class logoutUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        response = Response({'message': 'Logged out'})
        response.delete_cookie('auth_token')
        return response


class userDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.user)

        return Response('test')
