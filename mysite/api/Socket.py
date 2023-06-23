import tinytuya
import os
from datetime import datetime
import json
from threading import Thread
import time
from multiprocessing import Process
class Socket:
    Status="Offline"
    def __init__(self,key,ip,local_key):
        self.key=key
        self.ip=ip
        self.local_key=local_key
        self.initialzieSocket()
        
    
    def initialzieSocket(self):
        socket=tinytuya.OutletDevice(self.key,self.ip,self.local_key)
        socket.set_version(3.3)
        self.socket=socket

    
    def turn_on(self):
        self.socket.turn_on()

    
    def turn_off(self):
        self.socket.turn_off()

    
    def get_status(self):
        file_name=f"{os.getcwd()}/{self.key}.json"
        self.delete_created_file(file_name)
        proc=Process(target=self.try_to_save_status_to_file,args=())
        proc.start()
        time.sleep(3)
        proc.terminate()

        if self.status_file_created(file_name):
            data=json.load(open(file_name))
            self.status=data["status"]
            return self.status

        else:
            self.status="Offline"
            return self.status

    
    def try_to_save_status_to_file(self):
        file_name=f"{self.key}.json"
        socket_status=self.try_to_get_status()
        res={"status":socket_status,"time":str(datetime.now())}
        json.dump(res,open(file_name,"w"))


    def delete_created_file(self,file_name):
        try:
            os.remove(file_name)
        except:
            pass


    def status_file_created(self,file_name):
        if os.path.exists(file_name):
            return True
        else:
            return False
        
    
    def try_to_get_status(self):
        status=self.socket.status()["dps"]["1"]
        if status:
            return "On"
        else:
            return "Off"
