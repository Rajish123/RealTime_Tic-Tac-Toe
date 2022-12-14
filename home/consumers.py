from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

class GameRoom(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        # %s will be replaced by self.room_name
        self.room_group_name = 'room_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def receive(self,text_data):
        async_to_sync(self.channel_name.group_send)(
            self.room_group_name,{
                'type':'run_game',
                'payload':text_data
            }
        )

    def run_game(self,event):
        data = event['payload']
        data = json.loads(data)

        self.send(text_data = json.dumps({
            'payload':data['data']
        }))


    def disconnect(self):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )