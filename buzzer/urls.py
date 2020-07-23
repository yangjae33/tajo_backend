from django.urls import path
from .views import BuzzerView

urlpatterns = [
    # /user/signup/
    path('',BuzzerView.as_view()),
    path('<bus>/<stn>',BuzzerView.as_view())
]