from django.db import models

# Create your models here.


class Userotp(models.Model):
    email = models.EmailField()
    otp = models.IntegerField()
    
    def __str__(self):
        return self.email