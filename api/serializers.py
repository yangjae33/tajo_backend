from rest_framework import serializers
from .models import BusStation
from .models import Route

class StationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BusStation
        fields = '__all__'
        
class RouteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'