
from .models import User,Bus

from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class BusSerializer(serializers.HyperlinkedModelSerializer):
    class Meth:
        model = Bus
        fields = '__all__'