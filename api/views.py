from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,Http404
import json
import requests
from bs4 import BeautifulSoup

def arrinfo(request,busRouteID):
    if busRouteID:
        return HttpResponse('info : {}'.format(busRouteID))
    else:
        return HttpResponse('No busRouteId')

def arrdetail(request,busRouteId):
    key = 'I6tIvypzejp0BAk97%2Be7MMlQ8GxV7FBkI15CUSMc3WM0jQ834dsIKxgh5gCmaPWhGpXKuqYgbpd0ftq4f24RyQ%3D%3D'
    #busRouteId = '100100118'
    stn_id = '112000001'
    #queryParams = 'ServiceKey='+key+'&stId='+stn_id+'&busRouteId='+busRouteId+'&ord=18'
    queryParams = 'ServiceKey='+key+'&busRouteId='+busRouteId
    #경유노선 전체 정류소별 도착 예정 정보목록 조회url
    url = 'http://ws.bus.go.kr/api/rest/arrive/getArrInfoByRouteAll?'+queryParams
    #url = 'http://ws.bus.go.kr/api/rest/arrive/getArrInfoByRoute?'+queryParams
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

from .serializers import StationSerializer,RouteSerializer
from rest_framework import viewsets
from .models import BusStation , Route
from rest_framework.decorators import api_view
from rest_framework.response import Response


class RouteView(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

@api_view(['get'])
def route_view(request):
    routes = Route.objects.all()
    serializer = RouteSerializer(routes,context = {'request':request},many=True)
    return Response(serializer.data)

from rest_framework import viewsets
from rest_framework.views import APIView

class StationView(APIView):
    def get(self,request):
        data = json.loads(request.body)
        try:
            busRouteId=Route.objects.filter(route_nm=data['route_nm']).route_id
            key = 'e3xVi34VqCIVGHy5fE2BPPslceIcfj9xXO3hzCFB%2BMsL2cNTdfW4JBQjkUUrHYRLv%2FIajPlXV4D66RCZ1pzt9Q%3D%3D'
            queryParams = 'ServiceKey='+key+'&busRouteId='+busRouteId
            #노선별 경유 정류소 조회 서비스

            url = 'http://ws.bus.go.kr/api/rest/busRouteInfo/getStaionByRoute?'+queryParams
            req = requests.get(url)
            html = req.text
            
            soup = BeautifulSoup(html, 'html.parser')
            stn = soup.select('station')
            
            json_data = json.dumps(stn)
            return Response(json_data,status=200)
            
        except DoesNotExist:
            return Response(status=400) 

@api_view(['get'])
def station_view(request):
    stations = BusStation.objects.all()
    serializer = StationSerializer(stations,context = {'request':request},many=True)
    return Response(serializer.data)


class CheckStationView(APIView):
    def map_stn_name_id(self,name):
        try:
            return BusStation.objects.filter(stn_name=name)[:1].get()
        except BusStation.DoesNotExist:
            raise Http404

    def map_route_nm_id(self,name):
        try:
            return Route.objects.filter(route_nm=name)[:1].get()
        except Route.DoesNotExist:
            raise Http404
        
    def post(self,request):
        #request : route_nm, stn_name->stn_id
        data = json.loads(request.body)
        busRouteId = self.map_route_nm_id(data['route_nm']).route_id
        target_stn = self.map_stn_name_id(data['stn_name']).stn_id
        
        key = 'e3xVi34VqCIVGHy5fE2BPPslceIcfj9xXO3hzCFB%2BMsL2cNTdfW4JBQjkUUrHYRLv%2FIajPlXV4D66RCZ1pzt9Q%3D%3D'
        queryParams = 'ServiceKey='+key+'&busRouteId='+busRouteId
        #노선별 경유 정류소 조회 서비스

        url = 'http://ws.bus.go.kr/api/rest/busRouteInfo/getStaionByRoute?'+queryParams
        req = requests.get(url)
        html = req.text
        
        soup = BeautifulSoup(html, 'html.parser')
        stn = soup.select('station')
        
        for i in range (len(stn)):
            if stn[i].text == target_stn:
                return Response({"stn_id":target_stn},status=200)
            
        return Response({"message":"no matching station"},status=400)
    
    def get(self,request,*args,**kwargs):
        route_nm = self.kwargs['route_nm']
        busRouteId=self.map_route_nm_id(route_nm).route_id
        key = 'e3xVi34VqCIVGHy5fE2BPPslceIcfj9xXO3hzCFB%2BMsL2cNTdfW4JBQjkUUrHYRLv%2FIajPlXV4D66RCZ1pzt9Q%3D%3D'
        queryParams = 'ServiceKey='+key+'&busRouteId='+busRouteId
        #노선별 경유 정류소 조회 서비스

        url = 'http://ws.bus.go.kr/api/rest/busRouteInfo/getStaionByRoute?'+queryParams
        req = requests.get(url)
        html = req.text
            
        soup = BeautifulSoup(html, 'html.parser')
        stn = soup.select('station')
        stnNm = soup.select('stationNm')
        list_data = list()
        
        for i in range(len(stn)):
            json_data = dict()
            json_data['stn_id'] = stn[i].text
            json_data['stn_name'] = stnNm[i].text
            list_data.append(json_data)

        #print(list_data)    
        json_data = json.dumps(list_data)
        return_json_data = json.loads(json_data)
        return Response(return_json_data,status=200)
