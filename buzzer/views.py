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

from django.views.generic import TemplateView
from . import models
import json
from django.shortcuts import HttpResponse

class Alarm(TemplateView):
    template_name = "templates/alarm.html"

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data()
        context['username'] = self.request.user.username
        
        return context

class Reservation(TemplateView):
    template_name = "templates/reservation.html"

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data()
        context['username'] = self.request.user.username
        
        return context

    def post(self, request, **kwargs):
        ins=models.CallBuzzer()
        data_unicode = request.body.decode('utf-8')
        data=json.loads(data_unicode)
        ins.message = data['message']
        ins.save()

        return HttpResponse('')