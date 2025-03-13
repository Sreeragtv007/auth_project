from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Userotp


class userSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]


class UserotpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userotp
        fields = '__all__'
        
    def validate(self, attrs):
        return super().validate(attrs)
    
    def create(self, validated_data):
        userotp = Userotp.objects.filter(email=validated_data['email'])
        if userotp:
            userotp.update(otp=validated_data['otp'])
            return userotp
        else:
            return super().create(validated_data)
   
        

