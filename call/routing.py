from django.urls import path

from . import consumers

call_websocket_urlpatterns = [
    path(r"ws/call/<str:room_name>/<str:username>/", consumers.CallConsumer.as_asgi()),

]