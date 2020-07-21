# coding: utf-8

from django.db import models

class User(models.Model):
    #로그인 시 유저 ID
    user_id = models.CharField(max_length=50)
    #로그인 시 유저 PW
    user_password = models.CharField(max_length=255)
    #유저 이름
    user_name = models.CharField(max_length=50)

    def __str__(self):
        return self.user_name

    class Meta:
        db_table = "user"

class Bus(models.Model):
    
    #로그인 시 버스 ID : 번호판
    bus_id = models.CharField(max_length=50)
    #운행중인 노선 번호
    route_nm = models.CharField(max_length=20)
    #jwt
    bus_token = models.CharField(max_length=254)
    def __str__(self):
        return self.bus_id

    class Meta:
        db_table = "bus"


"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, PermissionsMixin
from django.utils import timezone

class UserManager(BaseUserManager):
    def _create_user(self,email,password,is_staff,is_superuser,**extra_fields):
        if not email:
            raise ValueError('Users must have an email')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            #email = email,
            email = email,
            is_staff = is_staff,
            is_superuser = is_superuser,
            last_login = now,
            data_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,email,password,**extra_fields):
        return self._create_user(email,password,False,False,**extra_fields)
    
    def create_superuser(self,email,password,**extra_fields):
        user = self._create_user(email,password,True,True,**extra_fields)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length = 254,unique=True)
    name = models.CharField(max_length=254,null=True,blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True,blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return f"/users/{self.pk}"


"""
