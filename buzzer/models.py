from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class CallBuzzer(models.Model):
    #버스 ID
    bus_id = models.CharField(max_length=150)
    #bus = models.ForeignKey('accounts.bus',on_delete=models.CASCADE,null=True,blank=True,default=None)
    #유저 idx
    user_id = models.CharField(max_length=150)
    #user = models.ForeignKey('accounts.user',on_delete=models.CASCADE,null=True,blank=True,default=None)
    #내릴 정류장
    stn_id = models.CharField(max_length=150)
    # #노선번호
    route_nm = models.CharField(max_length=50)
    #test
    message = models.CharField(max_length=100)

    arrive = models.CharField(max_length=100)
    """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    """
    def __str__(self):
        return self.bus
 
    class Meta:
        db_table = "Buzzer"
