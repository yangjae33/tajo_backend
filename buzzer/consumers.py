from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from .models import CallBuzzer



@receiver(post_save, sender=CallBuzzer)
def announce_stop(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "shares",{
                "type" : "share_message",
                "message" : instance.message,
            }
        )
        
class UserConsumer(WebsocketConsumer):

    def connect(self):
        self.groupname="shares"
        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            self.groupname,
            self.channel_name
        )
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.groupname,
            self.channel_name
        )
    def receive(self,text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.groupname,{
                'type': 'share_message',
                'message': message
            }
        )

    #recv msg from group
    def share_message(self,event):
        message = event['message']

        # send to ws
        self.send(text_data = json.dumps({
            'message': message
        }))