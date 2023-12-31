from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from datetime import datetime
from chat.models import *
from django.contrib.sessions.models import Session


class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        print("有人链接了")
        self.group_id = self.scope['url_route']['kwargs']['gid']
        self.uid = self.scope['url_route']['kwargs']['uid']
        async_to_sync(self.channel_layer.group_add)(self.group_id, self.channel_name)
        # 接受客户连接
        self.accept()

    def websocket_receive(self, message):
        # Send message to room group
        print("websocket_rreceive-----message------------------------------>")
        print(message)
        message['uid'] = str(self.uid)
        message['gid'] = str(self.group_id)
        async_to_sync(self.channel_layer.group_send)(
            self.group_id,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def websocket_disconnect(self, message):
        # 客户端主动断开连接时，触发
        print("断开连接")
        async_to_sync(self.channel_layer.group_discard)(
            self.group_id,
            self.channel_name
        )

    def chat_message(self, event):
        message = event['message']
        time = str(datetime.now().time())
        message['time'] = time
        self.send(text_data=json.dumps({"message": message}))
