from datetime import datetime, timedelta
import time
import clipboard
import schedule
from pathlib import Path
import argparse
import random
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
  init_action_config()
  time.sleep(2)
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

def init_action_config():
  global action_config_file
  action_config_data = open(action_config_file, "r")
  global action_config
  action_config = action_config_data.read()
  
def get_action_position(key):
  global action_config
  list = action_config.split("\n")
  for item in list:
    if item.startswith("#"):
      action_name = item[1:]
    else:
      if action_name == key:
        return item.split(",")
      
  Utils.print_with_datetime("[get_action_position: action point not init]")    
  return [0, 0]
  
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
    global chat_room_id
    if chat_room_id != "":
      update_count()
    result = check_live_list()
    if result == -1:
      login()
      break

def is_after_stream_dead_line():
  global stream_dead_line
  return datetime.now() > stream_dead_line

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
            item_chat_room_id = parse_dict(item, "chatRoomId")
            
            if item_live_room_id in white_list:
              if live_room_id != item_live_room_id:
                is_chat_room_changed = True
              
              chat_room_id = parse_dict(item, "chatRoomId")

              if live_room_id == "":
                stream_url = parse_dict(item, "rtmpLiveUrl")
                stream_url = stream_url.replace('artc://', 'rtmp://')
                global today_millis
                record_stream_command = "ffmpeg -y -i {} -acodec copy -vcodec copy {}-stream.mp4".format(stream_url, today_millis)
                print(record_stream_command)
                global keyword_header
                search_key_word = "{}{}".format(keyword_header, chat_room_id)
                print(search_key_word)
                time.sleep(10)

              live_room_id = item_live_room_id
              break
            else:
              Utils.print_with_datetime("{} :: {} :: {}-{}".format(item_live_room_id, item_chat_room_id, parse_dict(item, "nickName"), parse_dict(item, "liveName")))
          except:
            Utils.print_with_datetime("[check_live_list: data error]")
            continue
            
        if is_chat_room_changed:
          if len(chat_room_id) > 0:
            start_update()
          else:
            Utils.print_with_datetime("[check_live_list: chat room id error]")
            time.sleep(10)
            check_live_list()
        else:
          time.sleep(10)
      else:
        Utils.print_with_datetime("[check_live_list: live list empty]")
        reset_ids()
        time.sleep(10)
        check_live_list()
    elif code == 301:
      Utils.print_with_datetime("[check_live_list: need login]")
      return -1
    else:
      Utils.print_with_datetime("[check_live_list: check live list fail]")
      time.sleep(10)
      check_live_list()
  else:
    Utils.print_with_datetime("[check_live_list: request error]")
    time.sleep(10)
    check_live_list()

def start_update():
  global stream_dead_line
  global stream_duration_minute

  stream_dead_line = datetime.now() + timedelta(minutes = stream_duration_minute)
  
  init_count()

def init_count():
  global last_time
  last_time = round(time.time())
  global max_count
  
  global chat_room_id
  global temp_chat_room_list
  if chat_room_id in temp_chat_room_list:
    random_count = random.randint(-10 * 1000, 10 * 1000)
    max_count = 40 * 1000 + random_count
  else:
    random_count = random.randint(-30 * 1000, 30 * 1000)
    max_count = 220 * 1000 + random_count

def get_selected_count():
  click_input()
  time.sleep(.1)
  refresh_count()
  time.sleep(2)
  click_input()
  
  select_all()
  time.sleep(.1)
  
  copy_selected()
  selected = clipboard.paste()     
  return string_to_int(selected)

def string_to_int(value):
  try:
    result = int(value)
    return result
  except:
    return 0

def click_input():
  position = get_action_position("value_input_box")
  Utils.click_safely(string_to_int(position[0]), string_to_int(position[1]))

def refresh_count():
  Utils.hot_key_safely(["ctrl", "r"])

def update_count():
  time.sleep(.1)
  
  click_input()
  time.sleep(.1)
  refresh_count()
  time.sleep(2)

  click_input()
  time.sleep(.1)
  select_all()
  time.sleep(.1)
  
  copy_selected()

  try:
    current_count = int(clipboard.paste())
  except:
    current_count = -1

  global max_count
  global last_count
  global last_time
  
  if current_count < 0:
    time.sleep(10)
    return
  elif current_count == 0:
    time.sleep(1)
  elif current_count >= max_count:
    if current_count >= max_count * 1.2:
      duration = random.randint(20, 24)
      time.sleep(duration)
      add = random.randint(0, 100)
    else:
      duration = random.randint(16, 20)
      time.sleep(duration)
      add = random.randint(0, 400)
  elif current_count - last_count > 3000:
    Utils.print_with_datetime(current_count)
    last_count = current_count
    time.sleep(10)
  else:
    global chat_room_id
    global temp_chat_room_list
    if chat_room_id in temp_chat_room_list:
      duration = random.randint(12, 14)
      time.sleep(duration)
      add = random.randint(100, 500)
    else:
      if current_count < 10 * 1000:
        add = random.randint(1200, 1600)
      elif current_count > 120 * 1000 and current_count < 150 * 1000:
        duration = random.randint(2, 4)
        time.sleep(duration)
        add = random.randint(600, 1000)
      elif current_count > 150 * 1000 and current_count < 180 * 1000:
        duration = random.randint(3, 5)
        time.sleep(duration)
        add = random.randint(400, 800)
      elif current_count > 180 * 1000:
        duration = random.randint(8, 10)
        time.sleep(duration)
        add = random.randint(200, 600)
      else:
        duration = random.randint(1, 3)
        time.sleep(duration)
        add = random.randint(800, 1200)
    current_count += add

    click_input()
    time.sleep(.1)
    select_all()
    time.sleep(.1)
    Utils.write_safely(str(current_count), "")

    time.sleep(.1)
    save()

    now = round(time.time())
    Utils.print_with_datetime("+{} +{} {}".format(get_string_full_length(now - last_time, 2), get_string_full_length(add, 4), current_count))
    last_time = now
    last_count = current_count 

def get_string_full_length(value_int, max_length):
  return "{:<{}}".format(value_int, max_length)

def reset_ids():
  global live_room_id
  global chat_room_id
  live_room_id = ""
  chat_room_id = ""

def select_all():
  Utils.hot_key_safely(["command", "a"])

def copy_selected():
  Utils.hot_key_safely(["command", "c"])

def save():
  Utils.hot_key_safely(["ctrl", "s"])

if __name__=="__main__":
  try:
    init()
  except Exception as e:
    Utils.print_with_datetime("-cancel\n{}".format(e))
  except KeyboardInterrupt:
    None