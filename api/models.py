from django.db import models

class BusStation(models.Model):
    #역ID ( 표준 버스정류장 ID 9자리 정수 )
    std_id = models.CharField(max_length=30)
    #역 ID ( 5자리 정수, 고유값 )
    ars_id = models.CharField(max_length=30)
    #역 이름, 띄어쓰기는 .으로 구분
    st_name = models.CharField(max_length=50)
    #경도
    pos_x = models.DecimalField(max_digits=20,decimal_places=15)
    #위도
    pos_y = models.DecimalField(max_digits=20,decimal_places=15)

    def __str__(self):
        return self.ars_id

class Route(models.Model):
    #노선번호 ( 버스에 써있는 번호 ) 
    route_nm = models.CharField(max_length=20)
    #노선ID ( 노선 고유한 값 9자리 정수 )
    route_id = models.CharField(max_length=20)

    def __str__(self):
        return self.route_nm