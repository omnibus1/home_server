import time
import vlc
from pytube import YouTube
import os



class Player:
    song_queue=[]
    is_playing=False

    @staticmethod
    def add_song_to_queue(song):
        Player.song_queue.append(song)

    @staticmethod
    def play_songs():
        Player.is_playing=True

        while Player.song_queue:
            song=Player.song_queue.pop(0)
            print("Currently Playing: "+song.song_name+" in que:")
            print(Player.song_queue)
            song.play()
        print("ending, no more")
        Player.is_playing=False




class Song:
    def __init__(self,song_name):
        self.song_name=song_name
        self.file_name=song_name+".mp4"



    def play(self):
        print(os.getcwd(),"=============")
        vlc_instance=vlc.Instance()
        player=vlc_instance.media_player_new()
        print(os.getcwd,"--------------------------")
        print(self.file_name)
        media=vlc_instance.media_new(os.getcwd()+"/api/Songs/"+self.file_name)
        player.set_media(media)
        player.play()
        time.sleep(2.0)
        print(player.get_length())
        time.sleep(player.get_length()/1000)


    def __str__(self):
        return "Song name: " + self.song_name
