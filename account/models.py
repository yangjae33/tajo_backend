from django.db import models

class User(models.Model):
    user_idx = models.CharField(max_length=50)
    user_id = models.CharField(max_length=50)
    user_password = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50)

    def __str__(self):
        return self.user_idx

class Bus(models.Model):
    bus_id = models.CharField(max_length=50)
    route_nm = models.CharField(max_length=20)

    def __str__(self):
        return self.bus_id
