from django.http import Http404
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType

from .serializers import BuzzerSerializer
from .models import CallBuzzer

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

class BuzzerView(APIView):
    def get_object(self,stn,bus):
        try:
            return CallBuzzer.objects.filter(stn_id=stn).filter(bus_id=bus)
        except CallBuzzer.DoesNotExist:
            raise Http404

    def post(self,request):
        serializer = BuzzerSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors,status=400)
    
    def delete(self,request,stn,bus,format=None):
        tp = (stn,bus)
        buzzer = self.get_object(stn,bus)
        buzzer.delete()
        return Response(status=204)

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
        context['username'] = self.request.user.name
        
        return context

class Reservation(TemplateView):
    template_name = "templates/reservation.html"

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data()
        context['username'] = self.request.user.name
        return context

    def post(self, request, **kwargs):
        ins=models.CallBuzzer()
        data_unicode = request.body.decode('utf-8')
        data=json.loads(data_unicode)
        ins.message = data['message']
        ins.save()
        return HttpResponse('')
