from django.contrib import admin
from django.urls import path,include
from rest_framework import routers

from account.views import UserView,fetch_user
from api.views import *
from buzzer.views import buzzer_view,BuzzerView
from buzzer import views

router = routers.DefaultRouter()
router.register('users',UserView)
router.register('callbuzzer',BuzzerView)
router.register('station',StationView)
router.register('route',RouteView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
    path('user_view/',fetch_user),
    path('arr_view/info',arrinfo,{'busRouteID': None}),
    path('arr_view/<busRouteId>/',arrdetail),

    path('buzzer_view/',buzzer_view),
    path('station_view/',station_view),
    path('route_view/',route_view),
    path('station_chk/',station_chk),

    path('reservation',views.Reservation.as_view()),
    path('alarm',views.Alarm.as_view()),
]
