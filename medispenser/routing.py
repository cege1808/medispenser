from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from channels.auth import AuthMiddlewareStack
from core.consumers import EchoConsumer, TaskManagerConsumer
from utilities.task_manager import TaskManager

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)

    "websocket": AuthMiddlewareStack(
        URLRouter([
            # URLRouter just takes standard Django path() or url() entries.
            path("demo/stream", EchoConsumer),
            path("demo/<colour>", TaskManagerConsumer)
        ])
    ),
})
