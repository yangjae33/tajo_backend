from django.shortcuts import render
from django.http import HttpResponse
import requests

def index(request):
    return HttpResponse("<h1>Hello world</h1>")

def api_view(request):
    key = 'I6tIvypzejp0BAk97%2Be7MMlQ8GxV7FBkI15CUSMc3WM0jQ834dsIKxgh5gCmaPWhGpXKuqYgbpd0ftq4f24RyQ%3D%3D'
    busRouteId = '100100118'

    queryParams = 'ServiceKey='+key+'&busRouteId='+busRouteId
    url = 'http://ws.bus.go.kr/api/rest/arrive/getArrInfoByRouteAll?'+queryParams

    print(url)
    req = requests.get(url)
    print(type(req))
    html = req.text
    print(type(html))
    print(html[:150])
    return HttpResponse(html)