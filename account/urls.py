from django.urls import path
from .views import UserSignIn, UserSignUp, fetch_user

urlpatterns = [
    # /user/signup/
    path('user/signup/',UserSignUp.as_view()),

    # /user/signin/
    path('user/signin/',UserSignIn.as_view()),

    # /user/list/
    path('user/list/',fetch_user),

    # /bus/signup/
    #path('bus/signup/')
    
    # /bus/signin/
    #path('bus/signin/')
    
    # /bus/list/
]