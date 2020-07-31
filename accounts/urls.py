from django.urls import path
from .views import UserSignIn, UserSignUp, BusSignUp, BusSignIn,fetch_user 

urlpatterns = [
    # /user/signup/
    path('user/signup',UserSignUp.as_view()),

    # /user/signin/
    path('user/signin',UserSignIn.as_view()),

    # /user/list/
    #path('user/list',fetch_user),

    # /bus/signup/
    path('bus/signup',BusSignUp.as_view()),
    
    # /bus/signin/
    path('bus/signin',BusSignIn.as_view()),
    
    # /bus/list/
]