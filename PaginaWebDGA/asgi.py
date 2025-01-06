import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from DgaApp import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PainaWebDGA.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/data/', consumers.DataConsumer.as_asgi()),
        ])
    ),
})
