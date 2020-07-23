import json
import jwt
import bcrypt

from .serializers import UserSerializer
from .models import User,Bus
from tajo_backend.settings import SECRET_KEY

from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.views import View

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

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
        try:
            if User.objects.filter(user_id = data['user_id']).exists():
                return JsonResponse({'message' : 'existed ID'},status=400)

            User(
                user_id = data['user_id'],
                user_password = bcrypt.hashpw(data['user_password'].encode('utf-8'),bcrypt.gensalt()).decode("utf-8"),
                user_name = data['user_name']
            ).save()

            return JsonResponse({'message' : 'sign up completed'}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'key error'},status = 400)

class UserSignIn(View):
    
    def post(self,request):
        data = json.loads(request.body)

        try:
            if User.objects.filter(user_id = data['user_id']).exists():
                user = User.objects.get(user_id = data['user_id'])
                if bcrypt.checkpw(data['user_password'].encode('utf-8'), user.user_password.encode('utf-8')):
                    token = jwt.encode({'user' : user.user_idx},SECRET_KEY,algorithm='HS256').decode("utf-8")
                    return JsonResponse({'user_id':user_id,'token': token}, status = 200)
                else:
                    #wrong PW
                    return JsonResponse({'message':'wrong passowrd'}, status=401)

            # invalid ID
            return JsonResponse({'message':'invalid ID'},status=400)

        except KeyError:
            return JsonResponse({'message' : 'key error'},status = 400)

class BusSignUp(View):
    def post(self,request):
        data = json.loads(request.body)
        try:
            if Bus.objects.filter(bus_id = data['bus_id']).exists():
                return JsonResponse({'message' : 'existed ID'}, status=400)

            Bus(
                bus_id = data['bus_id'],
                bus_token = bcrypt.hashpw(data['bus_id'].encode('utf-8'),bcrypt.gensalt()).decode("utf-8"),
                route_nm = data['route_nm']
            ).save()

            return JsonResponse({'message' : 'sign up completed'}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'key error'})

class BusSignIn(View):
    def post(self,request):
        data = json.loads(request.body)

        try:
            if Bus.objects.filter(bus_id = data['bus_id']).exists():
                bus = Bus.objects.get(bus_id = data['bus_id'])
                token = jwt.encode({'bus' : bus.bus_id},SECRET_KEY,algorithm='HS256').decode("utf-8")
                return JsonResponse({'route_nm':bus.route_nm,'token':token}, status = 200)
                
            # invalid ID
            return JsonResponse({'message':'invalid ID'},status=400)

        except KeyError:
            return JsonResponse({'message' : 'key error'},status = 400)

