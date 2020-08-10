from django.http import Http404
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType

from .serializers import BuzzerSerializer
from .models import CallBuzzer

from api.models import Route

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import requests
from bs4 import BeautifulSoup

class BuzzerView(APIView):
    def get_object(self,stn,bus):            
        try:
            return CallBuzzer.objects.filter(stn_id=stn).filter(bus_id=bus)
        except CallBuzzer.DoesNotExist:
            raise Http404

    # 하차벨 예약 등록
    def post(self,request):
        data = json.loads(request.body)
        key = 'I6tIvypzejp0BAk97%2Be7MMlQ8GxV7FBkI15CUSMc3WM0jQ834dsIKxgh5gCmaPWhGpXKuqYgbpd0ftq4f24RyQ%3D%3D'
        busRouteId = Route.objects.filter(route_nm=data['route_nm'])[:1].get().route_id
        stn_id = data['stn_id']
        #queryParams = 'ServiceKey='+key+'&stId='+stId+'&busRouteId='+busRouteId+'&ord=18'
        queryParams = 'ServiceKey='+key+'&busRouteId='+busRouteId
        #경유노선 전체 정류소별 도착 예정 정보목록 조회url
        url = 'http://ws.bus.go.kr/api/rest/arrive/getArrInfoByRouteAll?'+queryParams
        req = requests.get(url)
        html = req.text
        #print(html)
        soup = BeautifulSoup(html, 'html.parser')
        
        stId = soup.select('stId')
        stNm = soup.select('stNm')
        arsId = soup.select('arsId')
        rtNm = soup.select('rtNm')

        #첫번째 도착예정 차량 번호판 정보
        plainNo1 = soup.select('plainNo1')
        #첫번째 도착예정 버스 도착정보메세지
        arrmsg1 = soup.select('arrmsg1')
        
        lst = []
        temp={}
        for i in range (len(stId)):
            if stId[i].text == stn_id:
                
                temp = {}
                temp['stn_id'] = stId[i].text
                temp['stn_name'] = stNm[i].text
                #temp['arsId'] = arsId[i].text
                temp['route_nm'] = rtNm[i].text
                temp['bus_id'] = plainNo1[i].text
                temp['message'] = arrmsg1[i].text
                print(temp)
                break

        serializer_dict = {}
        serializer_dict['user_id']=data['user_id']
        serializer_dict['bus_id']=temp['bus_id']
        serializer_dict['route_nm']=temp['route_nm']
        serializer_dict['stn_id']=temp['stn_id']
        serializer_dict['message']="ok"

        serializer = BuzzerSerializer(data=serializer_dict)
        if(serializer.is_valid()):
            serializer.save()
        else:
            print(serializer.errors)
        return Response(serializer.data,status=200)
        
    # 하차벨 누르기 & 삭제
    def delete(self,request,*args,**kwargs):
        stn = self.kwargs['stn_id']
        bus = self.kwargs['bus_id']
        buzzer = self.get_object(stn,bus)
        buzzer.delete()
        return Response(status=204)

    # 예약 현황 조회
    def get(self,request,*args,**kwargs):
        bus_id = self.kwargs['bus_id']
        callbuzzer=CallBuzzer.objects.filter(bus_id=bus_id)
        
        serializer = BuzzerSerializer(callbuzzer,many=True)
        
        return Response(serializer.data,content_type=u"application/json; charset=utf-8",status=200)

@api_view(['get'])
def buzzer_view(request):
    buzzers = CallBuzzer.objects.all()
    serializer = BuzzerSerializer(buzzers,context = {'request':request},many=True)

    return Response(serializer.data)
