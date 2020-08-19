import json
import requests
from bs4 import BeautifulSoup

from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,Http404

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.models import Bus,User
from .models import Route,BusStation
from .serializers import StationSerializer

AVG_DIST = 17208.19840976472
MIN_DIST_DIFF = 1.839398464653641e-07

class StationView(APIView):
    def get(self,request):
        data = json.loads(request.body)
        try:
            busRouteId=Route.objects.filter(route_nm=data['route_nm']).route_id
            key = '%2FcZci34ZZmRn%2B%2BFnVmpxlg3gJTLopLKjlrYQ2oQOnbD5l9LzVmgm3b6jINJgSsd%2BJjMap5XMOxgSV8x7OPtjFQ%3D%3D'
#            key = 'e3xVi34VqCIVGHy5fE2BPPslceIcfj9xXO3hzCFB%2BMsL2cNTdfW4JBQjkUUrHYRLv%2FIajPlXV4D66RCZ1pzt9Q%3D%3D'
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
        key='%2FcZci34ZZmRn%2B%2BFnVmpxlg3gJTLopLKjlrYQ2oQOnbD5l9LzVmgm3b6jINJgSsd%2BJjMap5XMOxgSV8x7OPtjFQ%3D%3D'
        #key = 'e3xVi34VqCIVGHy5fE2BPPslceIcfj9xXO3hzCFB%2BMsL2cNTdfW4JBQjkUUrHYRLv%2FIajPlXV4D66RCZ1pzt9Q%3D%3D'
        queryParams = 'ServiceKey='+key+'&busRouteId='+busRouteId
        #노선별 경유 정류소 조회 서비스

        url = 'http://ws.bus.go.kr/api/rest/busRouteInfo/getStaionByRoute?'+queryParams
        req = requests.get(url)
        html = req.text
        
        soup = BeautifulSoup(html, 'html.parser')
        stn = soup.select('station')
        print(stn)
        for i in range (len(stn)):
            if stn[i].text == target_stn:
                return Response({"stn_id":target_stn},status=200)
            
        return Response({"message":"no matching stations"},status=400)
    
    def get(self,request,*args,**kwargs):
        route_nm = self.kwargs['route_nm']
        busRouteId=self.map_route_nm_id(route_nm).route_id
        key = '%2FcZci34ZZmRn%2B%2BFnVmpxlg3gJTLopLKjlrYQ2oQOnbD5l9LzVmgm3b6jINJgSsd%2BJjMap5XMOxgSV8x7OPtjFQ%3D%3D'
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

class BusGPSView(APIView):

    def get(self,request):
        data = json.loads(request.body)
        busId = data['bus_id']
        print(busId)

        try:
            route_nm = Bus.objects.filter(bus_id=busId).get().route_nm
        except Bus.DoesNotExist:
            raise Http404
        try:
            busRouteId = Route.objects.filter(route_nm=route_nm).get().route_id
        except Route.DoesNotExist:
            raise Http404

        key = "%2FcZci34ZZmRn%2B%2BFnVmpxlg3gJTLopLKjlrYQ2oQOnbD5l9LzVmgm3b6jINJgSsd%2BJjMap5XMOxgSV8x7OPtjFQ%3D%3D"
        queryParams = 'ServiceKey='+key+'&busRouteId='+busRouteId

        url = "http://ws.bus.go.kr/api/rest/buspos/getBusPosByRtid?"+queryParams

        req = requests.get(url)
        html = req.text

        soup = BeautifulSoup(html, 'html.parser')
        bus_ids = soup.select('plainNo')
        pos_xs = soup.select('gpsX')
        pos_ys = soup.select('gpsY')
        list_data = list()
        pos_x = ""
        pos_y = ""
        for i in range(len(bus_ids)):
            if bus_ids[i].text == busId:
                pos_x = pos_xs[i].text
                pos_y = pos_ys[i].text

        if pos_x is not None:
            json_data = dict()
            json_data['bus_id']=busId
            json_data['pos_x'] = pos_x
            json_data['pos_y'] = pos_y
            json_data = json.dumps(json_data)
            return_json_data = json.loads(json_data)
            return Response(return_json_data,content_type=u"application/json; charset=utf-8",status=200)
            
        else:
            return Response({"message":"no matching bus_id"},status=400)

class StationGPSView(APIView):
    def sortbyDist(self,pos_x,pos_y):
        RETURN_CNT = 6
        user_x = float(pos_x)
        user_y = float(pos_y)
        mylist = list()
        try:
            stns = BusStation.objects.all()
        except BusStation.DoesNotExist:
            return mylist
        serializer = StationSerializer(stns,many=True)
        json_data = json.dumps(serializer.data)
        return_json_data = json.loads(json_data)
        

        for i in return_json_data:
            temp = dict()
            temp['stn_id'] = i['stn_id']
            temp['stn_name'] = i['stn_name']
            temp['pos_x'] = float(i['pos_x'])
            temp['pos_y'] = float(i['pos_y'])
            temp['dist'] = (float(i['pos_x'])-user_x)**2 + (float(i['pos_y'])-user_y)**2
            mylist.append(temp)
        res = sorted(mylist, key = lambda temp: (temp['dist']))
        
        return res[:RETURN_CNT]

    def get(self,request):
        data = json.loads(request.body)
        stn_id = data['stn_id']
        try:
            stns = BusStation.objects.get(stn_id=stn_id)
            serializer = StationSerializer(stns)  
            print(serializer)
            return Response(serializer.data,content_type=u"application/json; charset=utf-8",status=200)

        except BusStation.DoesNotExist:
            raise Http404

        return Response({"message":"no matching stn_id"},status=400)

    # 사용자의 위치에서 가까운 순으로 버스 정류장 정보 반환
    def post(self,request):
        data = json.loads(request.body)
        user_x = data['pos_x']
        user_y = data['pos_y']
        mylist = self.sortbyDist(user_x,user_y)
        if len(mylist) == 0:
            return Response({"message":"Bad Request"},status=400)
        json_data = json.dumps(mylist)
        return_json_data = json.loads(json_data)
        return Response(return_json_data, status=200)
