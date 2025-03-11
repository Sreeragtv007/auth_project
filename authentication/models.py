from django.db import models

# Create your models here.


class Userotp(models.Model):
    email = models.EmailField(unique=True)
    otp = models.IntegerField()
    password = models.CharField(max_length=20)
    
    def __str__(self):
        return self.email