from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from accounts.views import *
from api.views import *
from buzzer.views import *

router = routers.DefaultRouter()
router.register('users',UserView)

urlpatterns = [
    
    path('',include(router.urls)),
    path('api/auth',obtain_jwt_token),
    
    path('buzzer_view/',buzzer_view),
    
    path('accounts/',include('accounts.urls')),
    path('api/',include('api.urls')),
    path('buzzer/',include('buzzer.urls')),

]
