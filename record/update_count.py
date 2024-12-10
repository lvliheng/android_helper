from datetime import datetime, timedelta
import time
import clipboard
import schedule
from pathlib import Path
import os
import argparse
import random
import json
import requests

from utils import Utils

def init():
  parser = argparse.ArgumentParser()
  parser.add_argument("-k", "--keyword", help = "keyword header")
  parser.add_argument("-n", "--name", help = "application name")
  parser.add_argument("-p", "--path", help = "application path")

  global temp_chat_room_list
  temp_chat_room_list = ["181595984166913"]

  args = parser.parse_args()
  
  global keyword_header
  if args.keyword != None:
    keyword_header = args.keyword
  else:
    keyword_header = ""
    
  global application_name
  if args.name != None:
    application_name = args.name
  else:
    application_name = ""
    
  global application_path
  if args.path != None:
    application_path = args.path
  else:
    application_path = ""

  global stream_refresh_hour
  stream_refresh_hour = 1
  global stream_duration_minute
  stream_duration_minute = 30

  start_hour = 15
  start_minute = 20
  
  start_job(start_hour, start_minute)

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

  global root
  root = "D:\\_temp\\stream\\"
  Path(root).mkdir(parents = True, exist_ok = True)
  global live_config_file
  live_config_file = "{}{}".format(root, "live_config")
  check_config_file(live_config_file)
  global request_config_file
  request_config_file = "{}{}".format(root, "request_config")
  check_config_file(request_config_file)
  global action_config_file
  action_config_file = "{}{}".format(root, "action_config")
  check_config_file(action_config_file)
  
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
  global stream_url
  stream_url = ""

  print(f"------------{today}------------")
  init_action_config()
  time.sleep(2)
  check_application()
  time.sleep(2)
  init_config()
  time.sleep(2)
  
  check_state()
  print(f"------------{today}------------")

def check_config_file(file_path):
  if not Path(file_path).exists():
    open(file_path, "w")

def check_application():
  global application_name
  global application_path
  
  command = "tasklist | findstr \"{}\"".format(application_name)
  process_list = os.popen(command).readlines()
  if len(process_list) == 0:
    Utils.hot_key_safely(["win", "r"])
    time.sleep(.1)
    Utils.write_safely("\"{}\{}\"".format(application_path, application_name), "enter")
    time.sleep(5)
    
  if not is_application_visible():
    task_kill()
    time.sleep(1)
    check_application()

def task_kill():
  task_kill_command = "taskkill /f /im \"{}\"".format(application_name)
  os.system(task_kill_command)

def is_application_visible():
  position = get_action_position("setting_button")
  setting_button_pixel = Utils.get_pixel_safely(string_to_int(position[0]), string_to_int(position[1]))
  time.sleep(.1)
  return setting_button_pixel == (236, 245, 255)

def init_config():
  global live_config_file
  live_config_data = open(live_config_file, "r")
  global live_config
  live_config = live_config_data.read()
  
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
    if is_after_stream_dead_line():
      if not is_chat_room_valid():
        break
    else:
      if is_chat_room_valid():
        time.sleep(.1)
        click_window_top()
        time.sleep(.1)
        if is_list_open():
          update_count()
      
      check_live_list()

def is_after_stream_dead_line():
  global stream_dead_line
  return datetime.now() > stream_dead_line

def check_live_list():
  global request_config
  url = parse_json(request_config, "url")
  token = parse_json(request_config, "token")
  headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer {}".format(token)}
  body = {"mobile": ""}
  response = requests.post(url=url, headers=headers, json=body)
  code = response.status_code
  if code == 200:
    data = response.json()
    try:
      live = data["data"]["live"]
    except:
      Utils.print_with_datetime("[check_live_list: data error]")
      time.sleep(10)
      check_live_list()
    
    global live_config
    global live_room_id
    global chat_room_id
    if len(live) > 0:
      is_chat_room_changed = False
      for item in live:
        try:
          item_live_room_id = parse_dict(item, "liveRoomId")
          
          if item_live_room_id in live_config:
            if live_room_id != item_live_room_id:
              is_chat_room_changed = True
              
            live_room_id = item_live_room_id
            chat_room_id = parse_dict(item, "chatRoomId")
            break
          else:
            Utils.print_with_datetime("{}: {}-{}".format(item_live_room_id, parse_dict(item, "nickName"), parse_dict(item, "liveName")))
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
      Utils.print_with_datetime("[check_live_list: live list empty]")
      reset_ids()
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
  setup_list()

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

def setup_list():
  global last_count
  last_count = 0

  if not is_list_open():
    toogle_list()
    time.sleep(2)

  if is_list_open():    
    global chat_room_id
    if string_to_int(chat_room_id) == 0:
      time.sleep(10)
    else:
      check_id(chat_room_id)
  else:
    check_application()
    time.sleep(2)

def check_id(id):
  click_input_box()

  search(id)
  time.sleep(3)

  if is_chat_room_exists():
    click_selected_item()
    
    time.sleep(.1)
    if not is_chat_room_valid():
      if get_selected_count() == 0:
        time.sleep(1)
        return
      else:
        Utils.print_with_datetime("[check_id: chat room result ui invalid]")
        time.sleep(10)
        check_id(id)
  else:
    Utils.print_with_datetime("[check_id: chat room result data invalid]")
    time.sleep(10)
    check_id(id) 

def click_selected_item():
  position = get_action_position("selecte_item")
  Utils.click_safely(string_to_int(position[0]), string_to_int(position[1]))

def click_input_box():
  position = get_action_position("search_input_box")
  Utils.click_safely(string_to_int(position[0]), string_to_int(position[1]))

def search(id):
  select_all()
  time.sleep(.1)
  global keyword_header
  search_key_word = "{}{}".format(keyword_header, id)
  if Utils.write_safely(search_key_word, "enter") == False:
    time.sleep(1)  
    search(id)

def is_chat_room_exists():
  move_to_selected_item()
    
  time.sleep(.1)
  position = get_action_position("selecte_item")
  result_item_pixel = Utils.get_pixel_safely(string_to_int(position[0]), string_to_int(position[1]))
  time.sleep(.1)
  return result_item_pixel == (231, 231, 231)

def move_to_selected_item():
  position = get_action_position("selecte_item")
  Utils.move_to_safely(string_to_int(position[0]), string_to_int(position[1]))

def is_chat_room_valid():
  global chat_room_id
  
  time.sleep(.1)
  position = get_action_position("refresh_button")
  refresh_button_pixel = Utils.get_pixel_safely(string_to_int(position[0]), string_to_int(position[1]))
  time.sleep(.1)
  
  return chat_room_id != "" and refresh_button_pixel == (103, 194, 58) and get_selected_count() > 0

def get_selected_count():
  click_input()
  time.sleep(.1)
  refresh_count()
  time.sleep(2)
  click_input()
  
  select_all()
  time.sleep(.1)
  
  if not is_list_open():
    return 0
  copy_selected()
  selected = clipboard.paste()     
  return string_to_int(selected)

def string_to_int(value):
  try:
    result = int(value)
    return result
  except:
    return 0

def is_list_open():
  time.sleep(.1)
  position = get_action_position("load_all")
  load_all_button_pixel = Utils.get_pixel_safely(string_to_int(position[0]), string_to_int(position[1]))
  time.sleep(.1)
  return load_all_button_pixel == (245, 108, 108)

def click_window_top():
  position = get_action_position("window_top")
  Utils.click_safely(string_to_int(position[0]), string_to_int(position[1]))

def toogle_list():
  position = get_action_position("host_title")
  Utils.click_safely(string_to_int(position[0]), string_to_int(position[1]))

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
  
  if is_list_closed():
    return
  copy_selected()

  try:
    current_count = int(clipboard.paste())
  except:
    current_count = 0

  global max_count
  global last_count
  global last_time
  
  if current_count <= 0:
    time.sleep(1)
  elif current_count >= max_count:
    toogle_list()
    time.sleep(1)
  elif current_count - last_count > 3000:
    Utils.print_with_datetime(current_count)
    last_count = current_count
    if is_list_closed():
      return
    time.sleep(10)
  else:
    global chat_room_id
    global temp_chat_room_list
    if chat_room_id in temp_chat_room_list:
      duration = random.randint(12, 14)
      time.sleep(duration)
      add = random.randint(200, 600)
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
    if is_list_closed():
      return
    save()
      
    now = round(time.time())
    Utils.print_with_datetime("+{} +{} {}".format(get_string_full_length(now - last_time, 2), get_string_full_length(add, 4), current_count))
    last_time = now
    last_count = current_count 

def is_list_closed():
  if not is_list_open():
    time.sleep(1)
    toogle_list()
    time.sleep(1)
    return True
  else:
    return False

def get_string_full_length(value_int, max_length):
  return "{:<{}}".format(value_int, max_length)

def reset_ids():
  global live_room_id
  global chat_room_id
  live_room_id = ""
  chat_room_id = ""

def select_all():
  Utils.hot_key_safely(["ctrl", "a"])

def copy_selected():
  Utils.hot_key_safely(["ctrl", "c"])

def save():
  Utils.hot_key_safely(["ctrl", "s"])

if __name__=="__main__":
  try:
    init()
  except Exception as e:
    Utils.print_with_datetime("-cancel\n{}".format(e))
  except KeyboardInterrupt:
    None