
import random

from auth import settings
from django.core.mail import send_mail


def generateOtp():
    otp = random.randint(1000, 9999)
    return otp


def sendMail(email, otp, subject, message):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

    return True
