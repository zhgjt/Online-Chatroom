from django.urls import re_path

from chat import consumers

websocket_urlpatterns = {
    # re_path(r'room/(?P<group>\w+)$', consumers.ChatConsumer.as_asgi()),
    # re_path('room/', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<gid>\w+)/(?P<uid>\w+)/$', consumers.ChatConsumer.as_asgi()),

}