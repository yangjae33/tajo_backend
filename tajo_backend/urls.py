from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from accounts.views import *
from api.views import *
from buzzer.views import *

router = routers.DefaultRouter()
#router.register('users',UserView)
router.register('callbuzzer',BuzzerView)
router.register('station',StationView)
router.register('route',RouteView)

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('',include(router.urls)),

    path('api/auth',obtain_jwt_token),

    path('rest-auth/',include('rest_auth.urls')),
    path('rest-auth/registration',include('rest_auth.registration.urls')),

    path('accounts/',include('allauth.urls')),

    path('arr_view/info',arrinfo,{'busRouteID': None}),
    path('arr_view/<busRouteId>/',arrdetail),

    path('buzzer_view/',buzzer_view),
    path('station_view/',station_view),
    path('route_view/',route_view),
    path('station_chk/',station_chk),

    path('reservation/',Reservation.as_view()),
    path('alarm/',Alarm.as_view()),

]
