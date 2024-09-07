from datetime import datetime, timedelta
import pyautogui
import time
import clipboard
import schedule
from pathlib import Path
import os
import argparse
import random
import json

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
  stream_refresh_hour = 1
  global stream_duration_minute
  stream_duration_minute = 30

  start_hour = 19
  start_minute = 30
  
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
  global today_millis
  global try_times
  try_times = 0
  current_time = datetime.now()
  stream_dead_line = current_time + timedelta(hours = stream_refresh_hour)

  today = "{}-{}-{}".format(current_time.strftime("%Y"), current_time.strftime("%m"), current_time.strftime("%d"))
  today_millis = "{}-{}".format(today, current_time.strftime("%f"))

  global root
  root = "D:\_temp\stream\\"
  global directory
  directory = "{}{}".format(root, today)
  Path(directory).mkdir(parents = True, exist_ok = True)
  
  global chat_room_id
  chat_room_id = ""
  global stream_url
  stream_url = ""

  print(f"------------{today}------------")
  check_app()

  clipboard.copy("")
  set_config()
  time.sleep(1)
  check_stream_state()
  
  time.sleep(30)
  close_app()
  # shutdown_player()
  time.sleep(10)
  convert_video()
  print(f"------------{today}------------")

def check_app():
  if is_app_running():
    move_to_first_desktop()
    click_window_left_top()
    time.sleep(.1)
    
    if not is_stream_empty() and not is_stream_start() and not is_stream_end():
      check_page()
  else:
    launch_app()
    time.sleep(10)
    check_page()

def move_to_first_desktop():
  hot_key_safely(["ctrl", "win", "left"])
  time.sleep(.1)
  hot_key_safely(["ctrl", "win", "left"])
  time.sleep(.1)

def check_page():
  global try_times
  try_times = 0
  
  while True:
    stop_play()
    time.sleep(.1)
    yellow_pixel = get_pixel_safely(705, 934)
    time.sleep(.1)
    yellow_exist = yellow_pixel == (222, 197, 69)
    white_pixel = get_pixel_safely(232, 986)
    time.sleep(.1)
    white_exist = white_pixel == (255, 255, 255)
    if yellow_exist and white_exist:
      open_live_list()
      time.sleep(2)
      break
    else:
      try_times += 1
      if try_times > 3:
        close_app()
        time.sleep(10)
        launch_app()
        time.sleep(10)
        check_page()
        break
      else:
        drag_next()

def stop_play():
  click_safely(478, 540)

def open_live_list():
  click_safely(705, 862)

def drag_next():
  drag_to_safely(485, 900, 485, 200)

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

def is_after_stream_dead_line():
  global stream_dead_line
  return datetime.now() > stream_dead_line

def is_stream_empty():
  time.sleep(.1)
  first_item_cover_pixel = get_pixel_safely(320, 220)
  time.sleep(.1)
  white_pixel = get_pixel_safely(300, 620)
  time.sleep(.1)
  refresh_button_pixel = get_pixel_safely(430, 640)
  time.sleep(.1)
  return (first_item_cover_pixel == (238, 238, 238) or (white_pixel != (255, 255, 255) and refresh_button_pixel == (183, 89, 195)))

def is_stream_start():
  time.sleep(.1)
  pixel = get_pixel_safely(320, 220)
  time.sleep(.1)
  return pixel == (7, 193, 96)

def is_stream_end():
  time.sleep(.1)
  white_pixel = get_pixel_safely(300, 620)
  time.sleep(.1)
  purple_pixel = get_pixel_safely(330, 620)
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

def refresh():
  print_with_datetime("refresh")
  time.sleep(.1)
  first_item_cover_pixel = get_pixel_safely(320, 220)
  time.sleep(.1)
  refresh_button_pixel = get_pixel_safely(430, 640)
  time.sleep(.1)
  if refresh_button_pixel == (183, 89, 195):
    click_refresh()
  elif first_item_cover_pixel == (238, 238, 238):
    drag_refresh()
  else:
    drag_refresh()

def click_refresh():
  click_safely(430, 640)

def drag_refresh():
  drag_to_safely(485, 300, 485, 800)

def click_start():
  click_safely(320, 220)

def click_window_left_top():
  click_safely(550, 20)

def click_window_right_top():
  click_safely(1000, 20)

def click_stop():
  click_safely(330, 620)

def click_close_record_list():
  click_safely(860, 260)

def start_record():
  print_with_datetime("--start")

  global current_time
  global today
  global today_millis
  global stream_dead_line
  global stream_duration_minute

  current_time = datetime.now()
  today_millis = "{}-{}".format(today, current_time.strftime("%f"))
  stream_dead_line = datetime.now() + timedelta(minutes = stream_duration_minute)
  
  click_start()

  time.sleep(1)
  set_config()
  
  time.sleep(4)
  init_config()
  
  time.sleep(6)
  init_count()

  time.sleep(8)
  global try_times
  if not is_stream_end():
    try_times = 0
    check_stream_url()    

  time.sleep(10)
  try_times = 0
  check_stream_state()

def check_stream_url():
  global stream_url
  if stream_url.startswith("rtmp:"):
    start_record_screen()
    time.sleep(2)
    start_record_stream(stream_url)
  else:
    global try_times
    try_times += 1
    if try_times > 5:
      print_with_datetime("---fail")
    else:
      time.sleep(3)
      check_stream_url()

def start_record_screen():
  click_window_left_top()

  time.sleep(.1)
  if press_safely("f10") == False:
    time.sleep(1)
    start_record_screen()

def start_record_stream(stream_url):
  click_window_right_top()
  stop_command()

  global directory
  global today_millis

  record_stream_command = "ffmpeg -y -i {} -acodec copy -vcodec copy {}\{}-stream.mp4".format(stream_url, directory, today_millis)
  if write_safely(record_stream_command, "enter") == False:
    time.sleep(1)
    start_record_stream(stream_url)

def check_file():
  if not is_record_file_exists():
    global try_times
    try_times += 1
    if try_times <= 5:
      time.sleep(11)
      check_stream_url()
  else:
    click_window_left_top()
    
    if is_list_open():
      update_count()

def is_record_file_exists():
  global directory
  global today_millis
  record_file = Path("{}\{}-stream.mp4".format(directory, today_millis))
  return record_file.is_file() and os.path.getsize(record_file) > 0

def set_config():
  content = clipboard.paste()
  file = open("live_config", "w")
  file.write(content)
  file.close()

def init_config():
  try:
    file_name = "live_config"
    file = open(file_name, "r")
    config = file.read()
    if config == "":
      print_with_datetime("config file empty")
      return
    global chat_room_id
    chat_room_id = parse_json(config, "id")
    global stream_url
    stream_url = parse_json(config, "text")
  except:
    print_with_datetime("init config error: {}".format(config))

def parse_json(config, key):
  try:
    value = json.loads(config)
    return value[key]
  except:
    return ""

def stop_record():
  print_with_datetime("---stop")
  time.sleep(1)
  stop_record_stream()
  time.sleep(1)
  stop_record_screen()

def stop_record_screen():
  click_stop()
  
  time.sleep(1)
  stop_record_mm()
  time.sleep(1)
  click_close_record_list()

def stop_record_stream():
  click_window_right_top()
  if press_safely("q") == False:
    time.sleep(1)
    stop_record_stream()

def launch_player():
  click_window_right_top()
  stop_command()

  global app_package
  launch_player_command = "launch_player"
  if write_safely(launch_player_command, "enter") == False:
    time.sleep(1)
    launch_player()

def convert_video():
  click_window_right_top()
  stop_command()

  convert_video_command = "convert_video"
  if write_safely(convert_video_command, "enter") == False:
    time.sleep(1)
    convert_video()

def stop_command():
  hot_key_safely(["ctrl", "c"])

def stop_record_mm():
  hot_key_safely(["ctrl", "f10"])

def shutdown_player():
  shutdown_player_command = "mm api -v 0 shutdown_player"
  os.popen(shutdown_player_command)

def init_count():
  global last_count
  last_count = 0
  global last_time
  last_time = round(time.time())
  global max_count
  random_count = random.randint(-30 * 1000, 30 * 1000)
  max_count = 220 * 1000 + random_count

  if not is_list_open():
    toogle_list()
    time.sleep(2)

  if is_list_open():
    global try_times
    try_times = 0
    
    global chat_room_id
    if string_to_int(chat_room_id) == 0:
      print_with_datetime("chat room id error: {}".format(chat_room_id))
      if try_times > 3:
        return
      
      try_times += 1
      time.sleep(1)
      init_config()
      time.sleep(3)
      init_count()
    else:
      check_id(chat_room_id)
  else:
    print_with_datetime("open list error")
    time.sleep(3)
    init_count()

def check_id(id):
  global try_times
  if try_times > 3:
    print_with_datetime("chat room error")
    return
    
  click_enter()

  search(id)
  time.sleep(3)

  if is_chat_room_exists():
    click_selected_item()
    
    time.sleep(.1)
    if not is_chat_room_valid():
      try_times += 1
      check_id(id)
  else:
    try_times += 1
    check_id(id)

def click_selected_item():
  click_safely(996, 835)

def click_enter():
  click_safely(1024, 728)

def search(id):
  select_all()
  time.sleep(.1)
  global keyword_header
  search_key_word = "{}{}".format(keyword_header, id)
  if write_safely(search_key_word, "enter") == False:
    time.sleep(1)  
    search(id)

def is_chat_room_exists():
  move_to_selected_item()
    
  time.sleep(.1)
  pixel = get_pixel_safely(996, 835)
  time.sleep(.1)
  return pixel == (231, 231, 231)

def move_to_selected_item():
  move_to_safely(996, 835)

def is_chat_room_valid():
  time.sleep(.1)
  pixel = get_pixel_safely(1805, 660)
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
  pixel = get_pixel_safely(1122, 1039)
  time.sleep(.1)
  return pixel == (245, 108, 108)

def toogle_list():
  click_safely(1048, 652)

def click_input():
  click_safely(1600, 820)

def refresh_count():
  hot_key_safely(["ctrl", "r"])

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
  
  if is_list_closed_or_stream_end():
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
    print_with_datetime(current_count)
    last_count = current_count
    if is_list_closed_or_stream_end():
      return
    time.sleep(10)
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
    write_safely(str(current_count), "")

    time.sleep(.1)
    if is_list_closed_or_stream_end():
      return
    save()
      
    now = round(time.time())
    print_with_datetime("+{} +{} {}".format(get_string_full_length(now - last_time, 2), get_string_full_length(add, 4), current_count))
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
  hot_key_safely(["ctrl", "a"])

def copy_selected():
  hot_key_safely(["ctrl", "c"])

def save():
  hot_key_safely(["ctrl", "s"])

def print_with_datetime(text):
  print(datetime.now(), text)

def move_to_safely(x, y):
  try:
    pyautogui.moveTo(x, y)
    time.sleep(.1)
  except:
    time.sleep(1)
    move_to_safely(x, y)

def click_safely(x, y):
  try:
    pyautogui.moveTo(x, y)
    time.sleep(.1)
    pyautogui.click(x, y)
  except:
    time.sleep(1)
    click_safely(x, y)

def drag_to_safely(from_x, from_y, to_x, to_y):
  try:
    pyautogui.moveTo(from_x, from_y)
    time.sleep(.1)
    pyautogui.dragTo(to_x, to_y, 1, button = "left")
  except:
    time.sleep(1)
    drag_to_safely(from_x, from_y, to_x, to_y)

def hot_key_safely(args):
  try:
    pyautogui.hotkey(args)
  except:
    time.sleep(1)
    hot_key_safely(args)

def press_safely(key):
  try:
    pyautogui.press(key)
    return True
  except:
    return False

def write_safely(content, key):
  try:
    pyautogui.write(content)
    time.sleep(.1)
    if not key == "":
      pyautogui.press(key)
    return True
  except:
    return False

def get_pixel_safely(x, y):
  try:
    pixel = pyautogui.pixel(x, y)
    if type(pixel) == tuple:
      return pixel
    else:
      time.sleep(1)
      get_pixel_safely(x, y)
  except Exception as e:
    print_with_datetime("get pixel: error:\n{}".format(e))
    time.sleep(1)
    get_pixel_safely(x, y)
    
if __name__=="__main__":
  try:
    init()
  except Exception as e:
    print_with_datetime("-cancel\n{}".format(e))