from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json
import requests
from bs4 import BeautifulSoup

def arr_view(request):
    key = 'I6tIvypzejp0BAk97%2Be7MMlQ8GxV7FBkI15CUSMc3WM0jQ834dsIKxgh5gCmaPWhGpXKuqYgbpd0ftq4f24RyQ%3D%3D'
    busRouteId = '100100118'
    stId = '112000001'
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
    
    for i in range (len(stId)):
        temp = {}
        temp['stId'] = stId[i].text
        temp['stNm'] = stNm[i].text
        temp['arsId'] = arsId[i].text
        temp['rtNm'] = rtNm[i].text
        temp['plainno1'] = plainNo1[i].text
        temp['arrmsg1'] = arrmsg1[i].text
        lst.append(temp)
        
    json_str = json.dumps(lst)
    json_data = json.loads(json_str)
    
    #print(json_data)
    # newHtml = ""
    # for i in lst:
    #     temp = "<p>"
    #     temp = temp+(("정류장ID : "+i['stId']+"<br>")
    #     +("정류장이름 : "+i['stNm']+"<br>")
    #     +("ARS-ID : "+i['arsId']+"<br>")
    #     +("노선번호 : "+i['rtNm']+"<br>")
    #     +("첫번째 차량번호 : "+i['plainno1']+"<br>")
    #     +("도착 메세지 : "+i['arrmsg1']+"<br>")+("</p>"))
    #     newHtml=newHtml+temp
    #return HttpResponse(newHtml)

    return JsonResponse(json_data, safe=False)

def station_chk(request):
    key = 'e3xVi34VqCIVGHy5fE2BPPslceIcfj9xXO3hzCFB%2BMsL2cNTdfW4JBQjkUUrHYRLv%2FIajPlXV4D66RCZ1pzt9Q%3D%3D'
    busRouteId = '100100112'
    queryParams = 'ServiceKey='+key+'&busRouteId='+busRouteId
    #노선별 경유 정류소 조회 서비스
    url = 'http://ws.bus.go.kr/api/rest/busRouteInfo/getStaionByRoute?'+queryParams
    req = requests.get(url)
    html = req.text
    # soup = BeautifulSoup(html, 'html.parser')
    
    # stId = soup.select('stId')
    # stNm = soup.select('stNm')
    # arsId = soup.select('arsId')
    # rtNm = soup.select('rtNm')
    return HttpResponse(html)

from .serializers import StationSerializer,RouteSerializer
from rest_framework import viewsets
from .models import BusStation , Route
from rest_framework.decorators import api_view
from rest_framework.response import Response

class StationView(viewsets.ModelViewSet):
    queryset = BusStation.objects.all()
    serializer_class = StationSerializer

@api_view(['get'])
def station_view(request):
    stations = BusStation.objects.all()
    serializer = StationSerializer(stations,context = {'request':request},many=True)
    return Response(serializer.data)

class RouteView(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

@api_view(['get'])
def route_view(request):
    routes = Route.objects.all()
    serializer = RouteSerializer(routes,context = {'request':request},many=True)
    return Response(serializer.data)

