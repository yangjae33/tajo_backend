from rest_framework import serializers
from .models import CallBuzzer
from accounts.serializers import UserSerializer,BusSerializer
from accounts.models import User,Bus
from django.db import models

class BuzzerSerializer(serializers.ModelSerializer):
    
    #user = UserSerializer()
    #bus = BusSerializer()
    class Meta:
        model = CallBuzzer
        fields='__all__'
        
        fields = [
            "user_id",
            "bus_id",
            "stn_id",
            "route_nm",
            "message"
        ]
        #read_only_fields=('user_id','bus_id',)