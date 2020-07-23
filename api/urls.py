from django.urls import path
from .views import CheckStationView

urlpatterns = [
    #path('test',CheckStationView.as_view({'post':'map_stn'})),
    path('<rnm>/station',CheckStationView.as_view()),
]