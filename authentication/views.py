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

            return Response({'message': "otp sent to emial"})
        else:
            return Response({"message": "unexpexted error found while sending otp"})

    # def post(self, request):
    #     email = request.data.get('email')
    #     password = request.data.get('password')
    #     otp = generateOtp()
    #     request.data['otp'] = otp
    #     serializer = UserotpSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #     subject = f"Your OTP is {otp}"
    #     message = "OTP for Registration"
    #     mail = sendMail(email, otp, message, subject)
    #     if mail == True:
    #         if Userotp.objects.filter(email=email).exists():
    #             Userotp.objects.filter(email=email).update(otp=otp)
    #         else:
    #             serializer = UserotpSerializer(data=request.data)

    #             if serializer.is_valid():
    #                 serializer.save()
    #             else:
    #                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         return Response({'error': 'unexpexted error found'}, status=status.HTTP_400_BAD_REQUEST)

    #     return Response({'message': 'OTP sent to your email'}, status=status.HTTP_200_OK)


class verifyRegistration(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        if Userotp.objects.filter(email=email, otp=otp).exists():
            userotp = Userotp.objects.get(email=email, otp=otp)
            request.data['username'] = email
            request.data['password'] = userotp.password

            request.data.pop('email')
            request.data.pop('otp')
            try:

                user_obj = User.objects.create_user(
                    username=request.data['username'], password=request.data['password'])
            except Exception as e:
                return Response({"message": str(e)})

            return Response({"message": "user verified"})

        else:
            return Response({"message": "otp is invalid"}, status=status.HTTP_400_BAD_REQUEST)


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
