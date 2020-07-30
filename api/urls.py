from django.urls import path
from .views import CheckStationView,StationView

urlpatterns = [
    #path('test',CheckStationView.as_view({'post':'map_stn'})),
    path('route-station-chk',CheckStationView.as_view()),
    path('route-station/<route_nm>',CheckStationView.as_view())
]