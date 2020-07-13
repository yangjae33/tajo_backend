from django.db import models

class BusStation(models.Model):
    std_id = models.CharField(max_length=30)
    ars_id = models.CharField(max_length=30)
    st_name = models.CharField(max_length=50)
    pos_x = models.DecimalField(max_digits=20,decimal_places=15)
    pos_y = models.DecimalField(max_digits=20,decimal_places=15)

    def __str__(self):
        return self.ars_id

class Route(models.Model):
    route_nm = models.CharField(max_length=20)
    route_id = models.CharField(max_length=20)

    def __str__(self):
        return self.route_nm