from rest_framework import serializers
from .models import BusStation
from .models import Route

class StationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BusStation
        fields = [
            'stn_id',
            'ars_id',
            'stn_name',
            'pos_x',
            'pos_y'
        ]
        
class RouteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'