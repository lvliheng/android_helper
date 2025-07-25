from datetime import datetime, timedelta
import time
import clipboard
import schedule
from pathlib import Path
import os
import argparse
import random
import json
import base64

from utils import Utils

import pyautogui
pyautogui.FAILSAFE = False

def init():  
  parser = argparse.ArgumentParser()
  parser.add_argument("-p", "--package", help = "package name")
  parser.add_argument("-k", "--keyword", help = "keyword header")

  args = parser.parse_args()
  global app_package
  if args.package != None:
    app_package = args.package
  else:
    app_package = ""
  global keyword_header
  if args.keyword != None:
    keyword_header = args.keyword
  else:
    keyword_header = ""

  global stream_refresh_hour
  stream_refresh_hour = 2
  global stream_duration_minute
  stream_duration_minute = 30
  
  start_job([(14, 20), (19, 50)])

def start_job(times):
  global stream_refresh_hour
  global current_time

  for start_hour, start_minute in times:
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
  global today_millis
  global check_page_times
  check_page_times = 0
  global check_exists_times
  check_exists_times = 0
  global check_list_times
  check_list_times = 0
  
  current_time = datetime.now()
  stream_dead_line = current_time + timedelta(hours = stream_refresh_hour)

  today = "{}-{}-{}".format(current_time.strftime("%Y"), current_time.strftime("%m"), current_time.strftime("%d"))
  today_millis = "{}-{}".format(today, current_time.strftime("%f"))

  global directory
  directory = today
  Path(directory).mkdir(parents = True, exist_ok = True)
  global last_file_size
  last_file_size = -1
  global live_info_file
  live_info_file = "live_info"
  
  global live_config_file
  live_config_file = "live_config"
  check_config_file(live_config_file)
  global request_config_file
  request_config_file = "request_config"
  check_config_file(request_config_file)
  request_config_data = open(request_config_file, "r")
  global request_config
  request_config = request_config_data.read()
  
  global chat_room_id
  chat_room_id = ""
  global stream_url
  stream_url = ""

  print(f"------------{today}------------")  
  move_to_first_desktop()
  time.sleep(10)
  check_application()
  time.sleep(45)
  check_app()

  clipboard.copy("")
  set_config()
  time.sleep(1)
  check_stream_state()
  
  time.sleep(30)
  close_app()
  time.sleep(10)
  convert_video()
  print(f"------------{today}------------")

def check_application():
  click_window_right_top()
  time.sleep(.1)
  stop_command()

  check_application_command = "check_application"
  if Utils.write_safely(check_application_command, "enter") == False:
    time.sleep(1)
    check_application()

def check_app():
  if is_player_error():
    click_restart_player()
    time.sleep(45)
    check_app()
  else:
    if is_app_running():
      click_window_left_top()
      time.sleep(.1)
      
      if not is_stream_empty() and not is_stream_start() and not is_stream_end():
        check_page()
    else:
      launch_app()
      time.sleep(10)
      check_page()

def move_to_first_desktop():
  Utils.hot_key_safely(["ctrl", "win", "left"])
  time.sleep(.1)
  Utils.hot_key_safely(["ctrl", "win", "left"])
  time.sleep(.1)

def check_page():
  while True:
    stop_play()
    time.sleep(.1)
    yellow_pixel = Utils.get_pixel_safely(705, 934)
    time.sleep(.1)
    yellow_exist = yellow_pixel == (222, 197, 69)
    white_pixel = Utils.get_pixel_safely(232, 986)
    time.sleep(.1)
    white_exist = white_pixel == (255, 255, 255)
    if yellow_exist and white_exist:
      open_live_list()
      time.sleep(2)
      break
    else:
      global check_page_times
      check_page_times += 1
      if check_page_times > 3:
        close_app()
        time.sleep(10)
        reset_check_times()
        launch_app()
        time.sleep(10)
        check_page()
        break
      else:
        drag_next()

def stop_play():
  Utils.click_safely(478, 540)

def open_live_list():
  Utils.click_safely(705, 862)

def drag_next():
  Utils.drag_to_safely(485, 900, 485, 200)

def launch_app():
  global app_package
  launch_app_command = "mm api -v 0 launch_app {}".format(app_package)
  os.popen(launch_app_command)

def close_app():
  global app_package
  close_app_command = "mm api -v 0 close_app {}".format(app_package)
  os.popen(close_app_command)

def check_stream_state():
  while True:
    if is_player_error():
      click_restart_player()
      time.sleep(45)
      start()
      break
    else:
      if is_login_page_visible():
        Utils.print_with_datetime('-logout')
        login()
      else:
        if is_stream_start():
          start_record()
          break
        elif is_stream_end():
          stop_record()

          if is_after_stream_dead_line():
            break
          else:
            time.sleep(13)
            refresh()
            time.sleep(7)
        elif is_stream_empty():
          if is_after_stream_dead_line():
            break
          else:
            time.sleep(3)
            refresh()
            time.sleep(3)
            if is_stream_start():
              start_record()
              break
            else:
              time.sleep(7) 
        else:
          time.sleep(1)
          check_file()

def is_player_error():
  time.sleep(.1)
  red_icon_pixel = Utils.get_pixel_safely(406, 597)
  time.sleep(.1)
  restart_button_pixel = Utils.get_pixel_safely(284, 484)
  time.sleep(.1)
  return ((red_icon_pixel == (0, 209, 255) and restart_button_pixel == (255, 0, 104)))

def click_restart_player():
  Utils.click_safely(284, 484)

def is_after_stream_dead_line():
  global stream_dead_line
  return datetime.now() > stream_dead_line

def is_stream_empty():
  time.sleep(.1)
  first_item_cover_pixel = Utils.get_pixel_safely(320, 220)
  time.sleep(.1)
  white_pixel = Utils.get_pixel_safely(300, 620)
  time.sleep(.1)
  refresh_button_pixel = Utils.get_pixel_safely(430, 640)
  time.sleep(.1)
  return (first_item_cover_pixel == (238, 238, 238) or (white_pixel != (255, 255, 255) and refresh_button_pixel == (183, 89, 195)))

def is_stream_start():
  time.sleep(.1)
  pixel = Utils.get_pixel_safely(320, 220)
  time.sleep(.1)
  return pixel == (7, 193, 96)

def is_stream_end():
  time.sleep(.1)
  white_pixel = Utils.get_pixel_safely(480, 590)
  time.sleep(.1)
  purple_pixel = Utils.get_pixel_safely(480, 600)
  time.sleep(.1)
  return white_pixel == (255, 255, 255) and purple_pixel == (183, 89, 195)

def is_app_running():
  global app_package

  if app_package == "":
    return True

  app_state_command = "mm api -v 0 app_state {}".format(app_package)
  app_state = os.popen(app_state_command).readlines()
  if (len(app_state) > 0):
      result = app_state[len(app_state) - 1]
      if ("state=running" in result):
        return True
      else:
        return False
  else:
    return False

def check_config_file(file_path):
  if not Path(file_path).exists():
    open(file_path, "w")

def decode(encode_value):
  decode_bytes = base64.b64decode(encode_value.encode("ascii"))
  return decode_bytes.decode("ascii")

def parse_dict(data, key):
  try:
    if type(data) == dict:
      return data[key]
    else:
      return ""
  except:
    return ""
  
def is_login_page_visible():
  time.sleep(.1)
  is_white_match = Utils.is_pixel_match_color_safely(246, 474, (254, 254, 254))
  time.sleep(.1)
  is_password_button_match = Utils.is_pixel_match_color_safely(417, 760, (30, 37, 53))
  time.sleep(.1)
  return is_white_match and is_password_button_match

def click_dismiss_logout_tip_dialog():
  Utils.click_safely(405, 628)

def login():
  click_login_with_password()
  global request_config
  login_json = parse_json(request_config, "login")
  account = decode(parse_dict(login_json, "account"))
  password = decode(parse_dict(login_json, "password"))
  time.sleep(1)
  click_account_input()
  time.sleep(1)
  write_content_with_interval(account)
  time.sleep(1)
  click_password_input()
  time.sleep(1)
  write_content_with_interval(password)
  time.sleep(1)
  click_check_box()
  time.sleep(1)
  click_login()
  time.sleep(10)
  check_app()
  
def click_login_with_password():
  Utils.click_safely(417, 760)

def click_account_input():
  Utils.double_click_safely(341, 447)
  
def write_content(content):
  Utils.write_safely(str(content), "")

def write_content_with_interval(content):
  Utils.write_with_interval_safely(str(content), "")
 
def click_password_input():
  Utils.double_click_safely(248, 592)
  
def click_login():
  Utils.click_safely(408, 760)

def click_check_box():
  if not Utils.is_pixel_match_color_safely(303, 672, (38, 221, 105)):
    Utils.click_safely(303, 672)

def refresh():
  Utils.print_with_datetime("refresh")
  first_item_cover_pixel = Utils.get_pixel_safely(320, 220)
  time.sleep(.1)
  refresh_button_pixel = Utils.get_pixel_safely(430, 640)
  time.sleep(.1)
  if refresh_button_pixel == (183, 89, 195):
    click_refresh()
  elif first_item_cover_pixel == (238, 238, 238):
    drag_refresh()
  else:
    drag_refresh()

def click_refresh():
  Utils.click_safely(430, 640)

def drag_refresh():
  Utils.drag_to_safely(485, 300, 485, 800)

def click_start():
  Utils.click_safely(320, 220)

def click_window_left_top():
  Utils.click_safely(500, 20)

def click_window_right_top():
  Utils.click_safely(1000, 20)

def click_stop():
  button_pixel = Utils.get_pixel_safely(330, 620)
  background_pixel = Utils.get_pixel_safely(330, 520)
  if button_pixel == (183, 89, 195) and background_pixel == (255, 254, 255):
    click_dialog_button()
  else:
    click_close_button()

def click_dialog_button():
  Utils.click_safely(330, 620)
  
def click_close_button():
  Utils.click_safely(720, 110)

def click_close_record_list():
  Utils.click_safely(860, 260)

def start_record():
  Utils.print_with_datetime("--start")
  global current_time
  global today
  global today_millis
  global stream_dead_line
  global stream_refresh_hour

  current_time = datetime.now()
  today_millis = "{}-{}".format(today, current_time.strftime("%f"))
  stream_dead_line = datetime.now() + timedelta(hours = stream_refresh_hour)
  
  click_start()

  time.sleep(1)
  set_config()
  
  time.sleep(4)
  init_config()
  
  time.sleep(2)
  init_count()
  time.sleep(4)
  setup_list()

  time.sleep(8)
  if not is_stream_end():
    check_stream_url()    

  time.sleep(10)
  reset_check_times()
  check_stream_state()

def check_stream_url():
  global stream_url
  if stream_url.startswith("rtmp:"):
    start_record_screen()
    time.sleep(2)
    start_record_stream(stream_url)
  else:
    click_stop()
    time.sleep(10)

def is_record_started():
  pixel = Utils.get_pixel_safely(780, 60)
  time.sleep(.1)
  pixel2 = Utils.get_pixel_safely(810, 60)
  time.sleep(.1)
  return pixel == (255, 0, 104) or pixel2 == ((255, 0, 104))

def start_record_screen():
  click_window_left_top()

  time.sleep(.1)
  if is_record_started():
    stop_record_screen()
  time.sleep(1)
  if Utils.press_safely("f10") == False:
    time.sleep(1)
    start_record_screen()

def start_record_stream(stream_url):
  click_window_right_top()
  time.sleep(.1)
  stop_command()

  global directory
  global today_millis
  today_millis = "{}-{}".format(today, datetime.now().strftime("%f"))
  record_stream_command = "ffmpeg -y -i {} -acodec copy -vcodec copy {}\{}-stream.mp4".format(stream_url, directory, today_millis)
  if Utils.write_safely(record_stream_command, "enter") == False:
    time.sleep(1)
    start_record_stream(stream_url)

def reset_check_times():
  global check_page_times
  check_page_times = 0
  global check_exists_times
  check_exists_times = 0

def check_file():
  if not is_record_file_exists():
    Utils.print_with_datetime("[check_file: invalid]")
    time.sleep(11)
    
    if not is_record_file_exists():
      global last_file_size
      last_file_size = -1
      click_stop()
      time.sleep(10)
    else:
      check_file()
  else:
    click_window_left_top()
    
    time.sleep(.1)
    click_application_top()
    time.sleep(.1)
    if is_list_open():
      update_count()
    else:
      if not is_stream_end():
        setup_list()

def is_record_file_exists():
  global directory
  global today_millis
  record_file = Path("{}\{}-stream.mp4".format(directory, today_millis))
  
  if record_file.exists():
    current_file_size = os.path.getsize(record_file)
    
    global check_exists_times
    global last_file_size
    if current_file_size > 0:
      if current_file_size > last_file_size:
        check_exists_times = 0
        is_file_valid = True
      else:
        check_exists_times += 1
        if check_exists_times <= 3:
          is_file_valid = True
        else:
          is_file_valid = False
    else:
      is_file_valid = False
      
    last_file_size = current_file_size
    return record_file.is_file() and is_file_valid
  else:
    return False

def set_config():
  content = clipboard.paste()
  global live_info_file
  file = open(live_info_file, "w")
  file.write(content)
  file.close()

def init_config():
  try:
    global live_config_file
    live_config_data = open(live_config_file, "r")
    global live_config
    live_config = live_config_data.read()
    separator = ","
    global temp_chat_room_list
    temp_chat_room_list = separator.join(parse_json(live_config, "chatRoomList"))

    global live_info_file
    file = open(live_info_file, "r")
    config = file.read()
    if config == "":
      Utils.print_with_datetime("[init_config: config data empty]")
      return
    global chat_room_id
    chat_room_id = parse_json(config, "id")
    global stream_url
    stream_url = parse_json(config, "text")
  except:
    Utils.print_with_datetime("[init_config: config data error: {}]".format(config))

def parse_json(data, key):
  try:
    value = json.loads(data)
    return value[key]
  except:
    return ""

def stop_record():
  Utils.print_with_datetime("----end")
  time.sleep(1)
  stop_record_stream()
  time.sleep(1)
  click_stop()
  if is_record_started():
    stop_record_screen()

def stop_record_screen():
  time.sleep(1)
  stop_record_mm()
  time.sleep(1)
  click_close_record_list()

def stop_record_stream():
  click_window_right_top()
  time.sleep(.1)
  if Utils.press_safely("q") == False:
    time.sleep(1)
    stop_record_stream()

def launch_player():
  click_window_right_top()
  time.sleep(.1)
  stop_command()

  global app_package
  launch_player_command = "launch_player"
  if Utils.write_safely(launch_player_command, "enter") == False:
    time.sleep(1)
    launch_player()

def convert_video():
  click_window_right_top()
  time.sleep(.1)
  stop_command()

  convert_video_command = "convert_video"
  if Utils.write_safely(convert_video_command, "enter") == False:
    time.sleep(1)
    convert_video()

def stop_command():
  Utils.hot_key_safely(["ctrl", "c"])

def stop_record_mm():
  Utils.hot_key_safely(["ctrl", "f10"])

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
    max_count = 250 * 1000 + random_count

def setup_list():
  global last_count
  last_count = 0

  if not is_list_open():
    toogle_list()
    time.sleep(2)

  if is_list_open():    
    global chat_room_id
    if string_to_int(chat_room_id) == 0:      
      click_stop()
      time.sleep(10)
    else:
      check_id(chat_room_id)
  else:
    check_application()
    time.sleep(10)

def check_id(id):
  if id == "":
    click_stop()
    time.sleep(10)
    return
    
  click_enter()

  search(id)
  time.sleep(3)

  if is_chat_room_exists():
    click_selected_item()
    
    time.sleep(.1)
    if not is_chat_room_valid():
      if is_stream_end():
        time.sleep(1)
        stop_record()
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
  Utils.click_safely(996, 835)

def click_enter():
  Utils.click_safely(1024, 728)

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
  pixel = Utils.get_pixel_safely(996, 835)
  time.sleep(.1)
  return pixel == (231, 231, 231)

def move_to_selected_item():
  Utils.move_to_safely(996, 835)

def is_chat_room_valid():
  time.sleep(.1)
  pixel = Utils.get_pixel_safely(1805, 660)
  time.sleep(.1)
  return pixel == (103, 194, 58) and get_selected_count() > 0

def get_selected_count():
  click_input()
  time.sleep(.1)
  refresh_count()
  time.sleep(2)
  click_input()
  
  select_all()
  time.sleep(.1)
  
  if not is_list_open() or is_stream_end():
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
  pixel = Utils.get_pixel_safely(1122, 1039)
  time.sleep(.1)
  return pixel == (245, 108, 108)

def click_application_top():
  Utils.click_safely(1300, 620)

def toogle_list():
  Utils.click_safely(1048, 652)

def click_input():
  Utils.click_safely(1600, 820)

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
  
  if not is_list_open() or is_stream_end():
    return
  copy_selected()

  try:
    current_count = int(clipboard.paste())
  except:
    current_count = -1

  global max_count
  global last_count
  global last_time
  
  if current_count < 0:
    setup_list()
    time.sleep(1)
  elif current_count == 0:
    time.sleep(1)
  elif current_count - last_count > 3000:
    Utils.print_with_datetime(current_count)
    last_count = current_count
    if not is_list_open() or is_stream_end():
      return
    time.sleep(10)
  else:
    global chat_room_id
    global temp_chat_room_list
    if chat_room_id in temp_chat_room_list:
      duration = random.randint(12, 14)
      time.sleep(duration)
      add = random.randint(100, 500)
    else:
      if current_count >= max_count:
        if current_count >= max_count * 1.2:
          duration = random.randint(20, 24)
          time.sleep(duration)
          add = random.randint(0, 100)
        else:
          duration = random.randint(16, 20)
          time.sleep(duration)
          add = random.randint(0, 400)
      else:
        if current_count < 10 * 1000:
          add = random.randint(1200, 1600)
        elif current_count > 140 * 1000 and current_count < 180 * 1000:
          duration = random.randint(2, 4)
          time.sleep(duration)
          add = random.randint(600, 1000)
        elif current_count > 180 * 1000 and current_count < 220 * 1000:
          duration = random.randint(3, 5)
          time.sleep(duration)
          add = random.randint(400, 800)
        elif current_count > 220 * 1000:
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
    if not is_list_open() or is_stream_end():
      return
    save()
      
    now = round(time.time())
    Utils.print_with_datetime("+{} +{} {}".format(get_string_full_length(now - last_time, 2), get_string_full_length(add, 4), current_count))
    last_time = now
    last_count = current_count 

def is_list_closed_or_stream_end():
  if not is_list_open():
    time.sleep(1)
    toogle_list()
    time.sleep(1)
    return True
  elif is_stream_end():
    time.sleep(1)
    stop_record()
    time.sleep(1)
    return True
  else:
    return False

def get_string_full_length(value_int, max_length):
  return "{:<{}}".format(value_int, max_length)

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