from django.shortcuts import render
from .serializers import BuzzerSerializer
from rest_framework import viewsets
from .models import CallBuzzer
from rest_framework.decorators import api_view
from rest_framework.response import Response

class BuzzerView(viewsets.ModelViewSet):
    queryset = CallBuzzer.objects.all()
    serializer_class = BuzzerSerializer

@api_view(['get'])
def buzzer_view(request):
    buzzers = CallBuzzer.objects.all()
    serializer = BuzzerSerializer(buzzers,context = {'request':request},many=True)

    return Response(serializer.data)


