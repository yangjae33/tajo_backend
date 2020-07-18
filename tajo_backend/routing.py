from channels.routing import ProtocolTypeRouter, URLRouter
import buzzer.routing

application = ProtocolTypeRouter({
    'websocket':URLRouter(
        buzzer.routing.websocket_urlpatterns
    )
})