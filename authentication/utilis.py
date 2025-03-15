
import random
from rest_framework.authtoken.models import Token
from auth import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User


def generateOtp():
    otp = random.randint(1000, 9999)
    return otp


def sendMail(email, otp, subject, message):
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
    except :
        return False

    return True


def getuser(request):
    try:
        token = request.COOKIES.get('auth_token')

        tokenobj = Token.objects.get(key=token)
        
    except:
        return "please login"
    return tokenobj.user
