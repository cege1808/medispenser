from channels.consumer import SyncConsumer, AsyncConsumer
from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer, JsonWebsocketConsumer
import json
from channels.layers import get_channel_layer
from channels.worker import Worker
from utilities.task_manager import TaskManager
# from channels import Group

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


class TaskManagerConsumer(JsonWebsocketConsumer):

    groups = ['triggers']

    def connect(self):
        print("Someone connected")
        self.accept()

    def receive_json(self, content):
        if content['path'] == '/demo/':
            module_nums = [ content['module'] ]
            self.manager = TaskManager()
            self.manager.run_instruction(module_nums)
            self.send_json({'message': "Successfully ran task manager"})
        self.close()


    def disconnect(self, close_code):
        print(close_code)
