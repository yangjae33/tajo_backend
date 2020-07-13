from django.db import models

class CallBuzzer(models.Model):
    bus = models.CharField(max_length=50)
    user = models.CharField(max_length=50)
    #내릴 정류장
    station = models.CharField(max_length=50)
    def __str__(self):
        return self.bus_id