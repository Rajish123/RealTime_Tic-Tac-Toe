from django.urls import path
from .views import *

urlpatterns = [
    path("",home),
    path("play/<room_code>",play, name = 'play')
]
