from rest_framework import serializers
from .models import CallBuzzer

class BuzzerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CallBuzzer
        fields = '__all__'