from django.contrib import admin
from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
    path("play_song",views.play_song),
    path("song_queue",views.get_song_queue),
    path("avilable_songs",views.get_avilable_songs),
    path("remove_song",views.remove_song_from_queue),
    path("get_socket_status",views.get_socket_status),
    path("turn_on",views.turn_on),
    path("turn_off",views.turn_off),
    path("dont_run",views.dont_run_in_the_morning),
    path("do_run",views.do_run_in_the_morning),
    path("run_status",views.get_running_in_the_morning_status),
    path("jobs",views.get_jobs),
]