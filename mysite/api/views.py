from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import time
import json
from threading import Thread
import threading
from .song_player import Player
from .song_player import Player, Song
import glob
import os
from .Socket import Socket
from datetime import datetime
# Create your views here.

start_time=None

@api_view(["POST"])
def play_song(request):
    data=json.loads(request.body)

    Player.add_song_to_queue(Song(data["song_name"]))
    if not Player.is_playing:
        thread=Thread(target=Player.play_songs,args=())
        thread.start()

    return Response({"ok":"piosenka dodana"})

@api_view(["GET"])
def get_song_queue(request):
    response_dict={}
    song_queue=[str(song) for song in Player.song_queue]
    print(song_queue)
    response_dict["queue"]=song_queue
    print(response_dict)
    return Response(response_dict)

@api_view(["GET"])
def get_avilable_songs(request):
    base_path=os.getcwd()+"/api/Songs/"
    song_list=glob.glob(base_path+"*.mp4")
    song_list=[song.replace(base_path,"").replace(".mp4","") for song in song_list]

    response_dict={"avilable_songs":song_list}

    return Response(response_dict)

@api_view(["POST"])
def remove_song_from_queue(request):
    data=json.loads(request.body)
    print(data["song_name"])
    for song in Player.song_queue:
        if song.song_name==data["song_name"]:
            Player.song_queue.remove(song)
    response_dict={"status":"succesfull"}
    return Response(response_dict)

@api_view(["GET"])
def get_socket_status(request):
    socket=Socket("bf9616a76586eba918hgs2","10.0.1.31","d1c5d8102db020f8")
    status=socket.get_status()        
    return Response({"status":status})


@api_view(["GET"])
def turn_on(request):
    socket=Socket("bf9616a76586eba918hgs2","10.0.1.31","d1c5d8102db020f8")
    status=socket.get_status()
    if status=="Off":
        socket.turn_on()
        create_start_time_file(socket.key)
        return Response({"status":"succesfull, turned on"})
    elif status=="On":
        return Response({"status":"socket already on"})
    else:
        return Response({"status":"failed, socket offline"})

@api_view(["GET"])
def turn_off(request):
    socket=Socket("bf9616a76586eba918hgs2","10.0.1.31","d1c5d8102db020f8")
    status=socket.get_status()
    if status=="On":
        
        socket.turn_off()
        add_manual_job(socket.key)
        delete_time_file(socket.key)
        return Response({"status":"succesfull, turned off"})
    elif status=="Off":
        return Response({"status":"socket already off"})
    else:
        return Response({"status":"failed, socket offline"})
    

@api_view(["GET"])
def dont_run_in_the_morning(request):
    print(os.getcwd())
    file_path=f"{os.getcwd()}/run_config.json"
    data=json.load(open(file_path))
    data["run"]="False"
    json.dump(data,open(file_path,"w"),indent=4,separators=(',',': '))
    return Response({})

@api_view(["GET"])
def do_run_in_the_morning(request):
    print(os.getcwd())
    file_path=f"{os.getcwd()}/run_config.json"
    data=json.load(open(file_path))
    data["run"]="True"
    json.dump(data,open(file_path,"w"),indent=4,separators=(',',': '))
    return Response({})

@api_view(["GET"])
def get_running_in_the_morning_status(request):
    file_path=f"{os.getcwd()}/run_config.json"
    data=json.load(open(file_path))
    
    return Response(data)

@api_view(["GET"])
def get_jobs(request):
    jobs_path=f"{os.getcwd()}/jobs.json"
    job_list=json.load(open(jobs_path,"r"))
    job_list=job_list[::-1]
    return Response(job_list)

def create_start_time_file(socket_key):
    date=datetime.now()
    start_time=date.strftime("%d/%m/%Y %H:%M:%S")
    start_time_dict={"start_time":start_time}
    file_path=f"start_time_{socket_key}.json"
    json.dump(start_time_dict,open(file_path,"w"),indent=4,separators=(',',': '))

def add_manual_job(socket_key):
    jobs_path=f"{os.getcwd()}/jobs.json"
    file_path=f"start_time_{socket_key}.json"
    end_time=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    end_time=datetime.strptime(end_time,"%d/%m/%Y %H:%M:%S")


    data=json.load(open(file_path))
    start_time=datetime.strptime(data["start_time"],"%d/%m/%Y %H:%M:%S")

    duration=str(end_time-start_time)
    job={"status":"Succesfull","start_time":str(start_time),"end_time":str(end_time),"duration":duration,"type":"Manual"}
    try:
        jobList=json.load(open(jobs_path,"r"))
    except Exception as e:
        print(e)
        jobList=[]

    jobList.append(job)
    json.dump(jobList,open(jobs_path,"w"),indent=4,separators=(',',': '))

def delete_time_file(socket_key):
    file_path=f"start_time_{socket_key}.json"
    print(file_path,"---------------------")
    try:
        os.remove(file_path)
    except:
        pass


    


