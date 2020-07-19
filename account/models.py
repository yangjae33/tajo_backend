from django.db import models

class User(models.Model):
    #유저 고유값
    user_idx = models.CharField(max_length=50)
    #로그인 시 유저 ID
    user_id = models.CharField(max_length=50)
    #로그인 시 유저 PW
    user_password = models.CharField(max_length=50)
    #유저 이름
    user_name = models.CharField(max_length=50)

    def __str__(self):
        return self.user_idx

    class Meta:
        db_table = "user"

class Bus(models.Model):
    #버스 고유값
    bus_idx = models.CharField(max_length=50)
    #로그인 시 버스 ID
    bus_id = models.CharField(max_length=50)
    #운행중인 노선 번호
    route_nm = models.CharField(max_length=20)

    def __str__(self):
        return self.bus_id
