from datetime import datetime, timedelta
import time
import schedule
from pathlib import Path
import argparse
import json
import requests
import base64

from utils import Utils

def init():
  Utils.disable_fail_safe()
  
  parser = argparse.ArgumentParser()
  parser.add_argument("-k", "--keyword", help = "keyword header")

  args = parser.parse_args()
  
  global keyword_header
  if args.keyword != None:
    keyword_header = args.keyword
  else:
    keyword_header = ""

  global stream_refresh_hour
  stream_refresh_hour = 1
  global stream_duration_minute
  stream_duration_minute = 30

  start_hour = 19
  start_minute = 28
  
  # start_job(start_hour, start_minute)
  start()

def start_job(start_hour, start_minute):
  global stream_refresh_hour
  global current_time
  current_time = datetime.now()
  start_date_time = datetime(current_time.year, current_time.month, current_time.day, start_hour, start_minute)
  global end_date_time
  end_date_time = datetime(current_time.year, current_time.month, current_time.day, start_hour + stream_refresh_hour, start_minute)
  start_task_time = f"{start_hour:02d}:{start_minute:02d}"

  if current_time > start_date_time and current_time < end_date_time:
    start()
  else:
    print("-----task will start at {}-----".format(start_task_time))
  
  schedule.every().day.at(start_task_time).do(start)

  while True:
    schedule.run_pending()
    time.sleep(1)

def start():
  global stream_dead_line
  global stream_refresh_hour
  global current_time
  global today
  
  current_time = datetime.now()
  stream_dead_line = current_time + timedelta(hours = stream_refresh_hour)

  today = "{}-{}-{}".format(current_time.strftime("%Y"), current_time.strftime("%m"), current_time.strftime("%d"))
  global today_millis
  today_millis = "{}-{}".format(today, current_time.strftime("%f"))

  global root
  root = ""
  Path(root).mkdir(parents = True, exist_ok = True)
  global live_config_file
  live_config_file = "{}".format("live_config")
  check_config_file(live_config_file)
  global request_config_file
  request_config_file = "{}".format("request_config")
  check_config_file(request_config_file)
  global action_config_file
  action_config_file = "{}".format("action_config")
  check_config_file(action_config_file)
  global token_file
  token_file = "{}".format("token")
  check_config_file(token_file)
  
  global live_config
  live_config = ""
  global request_config
  request_config = ""
  global action_config
  action_config = ""
  global live_room_id
  live_room_id = ""
  global chat_room_id
  chat_room_id = ""

  global last_count
  last_count = 0

  print(f"------------{today}------------")
  init_config()
  time.sleep(2)
  
  global token
  token = get_token()
  if token == "":
    login()
  else:
    check_state()
  print(f"------------{today}------------")

def check_config_file(file_path):
  if not Path(file_path).exists():
    open(file_path, "w")

def init_config():
  global live_config_file
  live_config_data = open(live_config_file, "r")
  global live_config
  live_config = live_config_data.read()
  separator = ","
  global white_list
  white_list = separator.join(parse_json(live_config, "whiteList"))
  global temp_chat_room_list
  temp_chat_room_list = separator.join(parse_json(live_config, "chatRoomList"))
  
  global request_config_file
  request_config_data = open(request_config_file, "r")
  global request_config
  request_config = request_config_data.read()
  
def parse_json(data, key):
  try:
    if type(data) == str:
      value = json.loads(data)
      return value[key]
    else:
      return ""
  except:
    return ""
  
def parse_dict(data, key):
  try:
    if type(data) == dict:
      return data[key]
    else:
      return ""
  except:
    return ""

def check_state():
  while True:
    result = check_live_list()
    if result == -1:
      login()
      break

def login():
  global request_config
  login = parse_json(request_config, "login")
  url = parse_dict(login, "url")
  grant_type = parse_dict(login, "grantType")
  account = decode(parse_dict(login, "account"))
  password = decode(parse_dict(login, "password"))
  
  headers = {"Content-Type": "application/json; charset=utf-8"}
  body = {"grantType": grant_type, "userName": account, "password": password}
  response = requests.post(url = url, headers = headers, json = body)
  status_code = response.status_code
  if status_code == 200:
    data = response.json()
    code = data["code"]
    if code == 200:
      try:
        global token
        token = data["data"]["access_token"]
        if token != "":
          set_token()
          check_state()
      except:
        Utils.print_with_datetime("[login: data error]")
    else:
      Utils.print_with_datetime("[login: request error]")
    
def set_token():
  global token_file
  file = open(token_file, "w")
  global token
  file.write(token)
  file.close()
      
def decode(encode_value):
  decode_bytes = base64.b64decode(encode_value.encode("ascii"))
  return decode_bytes.decode("ascii")

def get_token():
  global token_file
  token_data = open(token_file, "r")
  token = token_data.read()
  token_data.close()
  return token

def check_live_list():
  global request_config
  live_json = parse_json(request_config, "live")
  url = parse_dict(live_json, "url")
  global token
  headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer {}".format(token)}
  body = {"mobile": ""}
  
  response = requests.post(url = url, headers = headers, json = body)
  status_code = response.status_code
  if status_code == 200:
    data = response.json()
    code = data["code"]
    if code == 200:
      try:
        live = data["data"]["live"]
      except:
        Utils.print_with_datetime("[check_live_list: data error]")
        time.sleep(10)
        check_live_list()
      
      global white_list
      global live_room_id
      global chat_room_id
      if len(live) > 0:
        is_chat_room_changed = False
        for item in live:
          try:
            item_live_room_id = parse_dict(item, "liveRoomId")
            
            if item_live_room_id in white_list:
              is_chat_room_changed = True
              
              chat_room_id = parse_dict(item, "chatRoomId")
              live_room_id = item_live_room_id
              Utils.print_with_datetime("->{}-{}".format(parse_dict(item, "nickName"), parse_dict(item, "liveName")))
              break
            else:
              Utils.print_with_datetime("{}-{}".format(parse_dict(item, "nickName"), parse_dict(item, "liveName")))
          except:
            Utils.print_with_datetime("[check_live_list: data error]")
            continue
            
        if is_chat_room_changed:
          if len(live_room_id) > 0:
            get_live_info()
            time.sleep(20)
          else:
            Utils.print_with_datetime("[check_live_list: chat room id error]")
            time.sleep(20)
            check_live_list()
        else:
          time.sleep(20)
      else:
        Utils.print_with_datetime("[check_live_list: live list empty]")
        reset_ids()
        time.sleep(20)
        check_live_list()
    elif code == 301:
      Utils.print_with_datetime("[check_live_list: need login]")
      return -1
    else:
      Utils.print_with_datetime("[check_live_list: check live list fail]")
      time.sleep(20)
      check_live_list()
  else:
    Utils.print_with_datetime("[check_live_list: request error]")
    time.sleep(20)
    check_live_list()

def get_live_info():
  global request_config
  live_json = parse_json(request_config, "live")
  global live_room_id
  url = "https://api.szbobo.net/video/api/room/realtimeInfo?liveRoomId={}".format(live_room_id)
  global token
  headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer {}".format(token)}
  
  response = requests.get(url = url, headers = headers)
  status_code = response.status_code
  if status_code == 200:
    data = response.json()
    code = data["code"]
    if code == 200:
      Utils.print_with_datetime("{} :: {}".format(data["data"]["userNum"], data["data"]["likeNum"]))

def reset_ids():
  global live_room_id
  global chat_room_id
  live_room_id = ""
  chat_room_id = ""

if __name__=="__main__":
  try:
    init()
  except Exception as e:
    Utils.print_with_datetime("-cancel\n{}".format(e))
  except KeyboardInterrupt:
    None