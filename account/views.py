import json

from .serializers import UserSerializer
from .models import User

from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['get'])
def fetch_user(request):
    users = User.objects.all()
    serializer = UserSerializer(users,context = {'request':request},many=True)

    return Response(serializer.data)

class UserSignUp(View):
    
    def post(self,request):
        data = json.loads(request.body)
        User(
            user_idx = data['user_idx'],
            user_id = data['user_id'],
            user_password = data['user_password'],
            user_name = data['user_name']
        ).save()

        return JsonResponse({'message' : 'sign up completed'},status=200)

class UserSignIn(View):
    
    def post(self,request):
        data = json.loads(request.body)

        if User.objects.filter(user_id = data['user_id']).exists():
            user = User.objects.get(user_id = data['user_id'])
            if user.user_password == data['user_password'] : 
                return JsonResponse({'message':f'Hi, {user.user_name}!'},status = 200)
            else:
                return JsonResponse({'message':'wrong passowrd'},status=200)

        return JsonResponse({'message':'invalid ID'},status=200)