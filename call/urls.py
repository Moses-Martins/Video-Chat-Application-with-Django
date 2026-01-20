from django.urls import path

from . import views

urlpatterns = [
    path("call/", views.videocall_index, name="videocall_index"),
    path("call/<str:room_name>/<str:username>/", views.videocall_room, name="videocall_room",
    ),
]
