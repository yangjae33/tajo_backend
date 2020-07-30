from django.urls import path
from .views import BuzzerView

urlpatterns = [
    path('',BuzzerView.as_view()),
    path('<bus_id>/<stn_id>',BuzzerView.as_view())
]