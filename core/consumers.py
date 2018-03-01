from channels.consumer import SyncConsumer, AsyncConsumer
from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer, JsonWebsocketConsumer
import json
# from channels.layers import get_channel_layer
from channels.worker import Worker
from medispenser._celery import run_motor, app

class EchoConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("websocket connect")
        print(event)
        await self.send({
            'type': 'websocket.accept',
        })

    async def websocket_receive(self, event):
        print("websocket recieve")
        print(event)
        await self.send({
            'type': 'websocket.send',
            "text": 'hello from server',
        })


class TaskManagerConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        print("Connection made")
        await self.accept()
        """
        Called when the websocket is handshaking as part of initial connection.
        """
        # Are they logged in?
        # if self.scope["user"].is_anonymous:
        #     # Reject the connection
        #     print("Reject connection")
        #     await self.close()
        # else:
        #     # Accept the connection
        #     print("Connection made")
        #     await self.accept()

    async def receive_json(self, content):
        if content['path'] == '/demo/':
            module_nums = [ content['module'] ]
            res = run_motor.delay(module_nums).get()
            await self.send_json({'message': res })
        await self.close()


    async def disconnect(self, close_code):
        print(close_code)
