from datetime import datetime
import json

file_path="/home/krzysztof/Desktop/nauka/home/home_server/mysite/startup.json"

run_dict={"run":"False"}
json.dump(run_dict,open(file_path,"w"))