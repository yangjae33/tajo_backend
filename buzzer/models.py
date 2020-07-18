from django.db import models

class CallBuzzer(models.Model):
    #버스 ID
    bus_id = models.CharField(max_length=50)
    #유저 idx
    user_id = models.CharField(max_length=50)
    #내릴 정류장
    station = models.CharField(max_length=50)
    
    #test
    message = models.CharField(max_length=100)

    def __str__(self):
        return self.bus_id