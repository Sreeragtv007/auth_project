
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import Userotp
from .serializers import UserotpSerializer, userSerilaizer
from authentication.utilis import generateOtp, sendMail, getuser
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.authtoken.models import Token


class userRegister(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        otp = generateOtp() # custom function to genrate otp
        data['otp'] = otp
        serializer = UserotpSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            subject = f"Your OTP is {otp}"
            message = "OTP for Registration"
            try:
                mail = sendMail(data['email'], otp, message, subject) # custom function to send otp via email
            except:
                return Response({"message": "unexpected error found while sending otp"}, status=status.HTTP_400_BAD_REQUEST)
            if mail == True:
                return Response({"message": "otp sent to mail"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "unexpected error found while sending otp"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors)


class verifyRegistration(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        if not email or not otp:
            return Response({"message": "Email and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            otp_obj = Userotp.objects.get(email=email, otp=otp)
        except:
            return Response({"message": "invalid otp"})

        if otp_obj:
            password = str(otp_obj.password)

            if User.objects.filter(username=email).exists():
                user = User.objects.get(username=email)
                user.set_password(str(otp_obj.password))
                user.save()
                otp_obj.delete()
                return Response({"message": "otp verified user created"},status=status.HTTP_201_CREATED)
            try:

                user = User.objects.create_user(
                    username=email, password=password)
                otp_obj.delete()

            except Exception as e:
                return Response({"message": str(e)})
            return Response({"message": "otp verified user created"},status=status.HTTP_201_CREATED)


class loginUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        password = request.data.get('password')
        email = request.data.get('email')
        if not email or not password:
            return Response({"message": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=email, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            response = Response({'message': 'Login successful'})
            response.set_cookie(
                key='auth_token',
                value=token.key,

                httponly=True,
                samesite='Lax',
                secure=True
            )
            return response
        return Response({'error': 'Invalid credentials'},status=status.HTTP_400_BAD_REQUEST)


class logoutUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        response = Response({'message': 'Logged out'},status=status.HTTP_200_OK)
        response.delete_cookie('auth_token')
        return response


class userDetail(APIView):

    permission_classes = [IsAuthenticated] # modified the default isauthenticated class

    def get(self, request):
        user = getuser(request) # custom function to get the authencated user
        

        return Response({"message": "user details", "logged in user": str(user)},status=status.HTTP_200_OK)
