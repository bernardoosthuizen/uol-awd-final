from channels.routing import ProtocolTypeRouter, ChannelNameRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import eLearningApp.routing

application = ProtocolTypeRouter({
        'websocket': AuthMiddlewareStack(
            URLRouter(
                eLearningApp.routing.websocket_urlpatterns
            )
        ),
    }) 