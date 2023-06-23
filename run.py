from datetime import datetime
import json
import time
import sys

sys.path.insert(1,"/home/krzysztof/Desktop/nauka/home/home_server/mysite/api")

import Socket

run_config=json.load(open("/home/krzysztof/Desktop/nauka/home/home_server/mysite/run_config.json"))

url_data=json.load(open("/home/krzysztof/Desktop/nauka/home/home_server/frontend/my-app/src/Config.json"))
base_url=url_data["IP_ADDRESS"]

jobs_path="/home/krzysztof/Desktop/nauka/home/home_server/mysite/jobs.json"

MAX_TRIES=5
DURATION=run_config["duration"]



def write_to_json(status,start_time,type):
    end_time=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    end_time=datetime.strptime(end_time,"%d/%m/%Y %H:%M:%S")
    start_time=datetime.strptime(start_time,"%d/%m/%Y %H:%M:%S")

    if type==1:
        duration=str(end_time-start_time)
    else:
        duration="-"
    job={"status":status,"start_time":str(start_time),"end_time":str(end_time),"duration":duration,"type":"Automatic"}
    try:
        jobList=json.load(open(jobs_path,"r"))
    except Exception as e:
        print(e)
        jobList=[]

    jobList.append(job)
    json.dump(jobList,open(jobs_path,"w"),indent=4,separators=(',',': '))

    
def main():
    date=datetime.now()
    start_time=date.strftime("%d/%m/%Y %H:%M:%S")
    if run_config["run"]=="True":

        socket=Socket.Socket("bf9616a76586eba918hgs2","10.0.1.31","d1c5d8102db020f8")
        status=socket.get_status()
        print(status)
        tries=0
        while status=="Offline":

            time.sleep(5)
            status=socket.get_status()
            tries+=1
            print(f"socket offline tried {tries}/{MAX_TRIES} times")
            if tries==MAX_TRIES:
                write_to_json("Failed",start_time,0)
                exit()
        print("socket online")
        socket.turn_on()
        print(DURATION)
        # time.sleep(DURATION)*60

        status=socket.get_status()
        time.sleep(2)
        if status=="Offline":
            write_to_json("Failed",start_time,0)
            exit()

        socket.turn_off()
        write_to_json("Succesfull",start_time,1)
        exit()

    else:
        print("Not running")
        write_to_json("Not run",start_time,0)
        exit()
        
    
if __name__=='__main__':
    main()
