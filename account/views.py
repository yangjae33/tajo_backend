from django.shortcuts import render
from .serializers import UserSerializer
from rest_framework import viewsets
from .models import User
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