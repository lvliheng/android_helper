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
  global app_package
  parser = argparse.ArgumentParser()
  parser.add_argument("-p", "--package", help = "package name")

  args = parser.parse_args()
  if args.package != None:
    app_package = args.package
  else:
    app_package = ""

  global stream_refresh_hour
  stream_refresh_hour = 1
  global stream_duration_minute
  stream_duration_minute = 30

  start_hour = 19
  start_minute = 30
  
  start_job(start_hour, start_minute)

def start_job(start_hour, start_minute):
  global stream_refresh_hour
  global current
  current = datetime.now()
  start_date_time = datetime(current.year, current.month, current.day, start_hour, start_minute)
  global end_date_time
  end_date_time = datetime(current.year, current.month, current.day, start_hour + stream_refresh_hour, start_minute)
  start_task_time = f"{start_hour:02d}:{start_minute:02d}"

  if current > start_date_time and current < end_date_time:
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
  global current
  global today
  global today_millis
  global try_times
  try_times = 0
  current = datetime.now()
  stream_dead_line = current + timedelta(hours = stream_refresh_hour)

  today = "{}-{}-{}".format(current.strftime("%Y"), current.strftime("%m"), current.strftime("%d"))
  today_millis = "{}-{}".format(today, current.strftime("%f"))

  global root
  root = "D:\_temp\stream\\"
  global directory
  directory = "{}{}".format(root, today)
  Path(directory).mkdir(parents = True, exist_ok = True)

  global file_name_tail_stream
  file_name_tail_stream = "stream"
  
  global chat_room_id
  chat_room_id = ""
  global stream_url
  stream_url = ""

  print(f"------------{today}------------")
  if is_app_running():
    time.sleep(3)
    pyautogui.hotkey("ctrl", "win", "left")
    time.sleep(1)
    pyautogui.hotkey("ctrl", "win", "left")
    time.sleep(1)
    click_window_left_top()
    time.sleep(1)
  # else:
  #   launch_player()
  #   time.sleep(120)

  clipboard.copy("")
  refresh()
  time.sleep(1)
  check_stream_state()
  # shutdown_player()
  
  time.sleep(20)
  convert_video()
  print(f"------------{today}------------")

def check_stream_state():
  while True:
    if not is_app_running():
      if is_after_stream_dead_line():
        break
      else:
        time.sleep(10)
        continue
    elif is_stream_start():
      start_record()
      break
    elif is_stream_end():
      stop_record()

      if is_after_stream_dead_line():
        break
      else:
        time.sleep(3)
        refresh()
        time.sleep(7)
    elif is_stream_empty():
      if is_after_stream_dead_line():
        break
      else:
        print_with_datetime("refresh")
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
  first_item_cover_pixel = pyautogui.pixel(320, 220)
  time.sleep(.1)
  refresh_button_pixel = pyautogui.pixel(430, 640)
  return (refresh_button_pixel == (183, 89, 195) or first_item_cover_pixel == (238, 238, 238))

def is_stream_start():
  time.sleep(.1)
  pixel = pyautogui.pixel(320, 220)
  return pixel == (7, 193, 96)

def is_stream_end():
  time.sleep(.1)
  pixel = pyautogui.pixel(330, 620)
  return pixel == (183, 89, 195)

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
  time.sleep(.1)
  first_item_cover_pixel = pyautogui.pixel(320, 220)
  time.sleep(.1)
  refresh_button_pixel = pyautogui.pixel(430, 640)
  if refresh_button_pixel == (183, 89, 195):
    click_refresh()
  elif first_item_cover_pixel == (238, 238, 238):
    drag_refresh()
  else:
    drag_refresh()

def click_refresh():
  pyautogui.click(430, 640)

def drag_refresh():
  pyautogui.moveTo(485, 300)
  pyautogui.dragTo(485, 800, 1, button = "left")

def click_start():
  pyautogui.moveTo(320, 220)
  time.sleep(.1)
  pyautogui.click(320, 220)

def click_window_left_top():
  pyautogui.click(550, 20)

def click_window_right_top():
  pyautogui.click(1000, 20)

def click_stop():
  pyautogui.click(330, 620)

def click_close_record_list():
  pyautogui.click(860, 260)

def start_record():
  print_with_datetime("--start")

  global current
  global today
  global today_millis
  global stream_dead_line
  global stream_duration_minute

  current = datetime.now()
  today_millis = "{}-{}".format(today, current.strftime("%f"))
  stream_dead_line = datetime.now() + timedelta(minutes = stream_duration_minute)
  
  click_start()

  time.sleep(1)
  setLiveConfig()
  
  time.sleep(1)
  initConfig()
  
  time.sleep(1)
  initCount()

  time.sleep(20)
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

  time.sleep(1)
  pyautogui.press("f10")

def start_record_stream(stream_url):
  click_window_right_top()
  pyautogui.hotkey("ctrl", "c")

  global directory
  global today_millis
  global file_name_tail_stream

  record_stream_command = "ffmpeg -y -i {} -acodec copy -vcodec copy {}\{}-{}.mp4".format(stream_url, directory, today_millis, file_name_tail_stream)
  pyautogui.write(record_stream_command)
  time.sleep(.1)
  pyautogui.press("enter")

def check_file():
  global file_name_tail_stream
  if not is_record_file_exists(file_name_tail_stream):
    global try_times
    try_times += 1
    if try_times <= 5:
      time.sleep(11)
      check_stream_url()
  else:
    click_window_left_top()
    
    if isListOpen():
      time.sleep(.1)
      updateCount()

def is_record_file_exists(type):
  global directory
  global today_millis
  record_file = Path("{}\{}-{}.mp4".format(directory, today_millis, type))
  return record_file.is_file() and os.path.getsize(record_file) > 0

def setLiveConfig():
  content = clipboard.paste()
  f = open("live_config", "w")
  f.write(content)
  f.close()

def initConfig():
  try:
    file_name = "live_config"
    f = open(file_name, "r")
    config = f.read()
    global chat_room_id
    chat_room_id = parseJson(config, "id")
    global stream_url
    stream_url = parseJson(config, "text")
  except:
    print("init config error:", config)

def parseJson(config, key):
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
  pyautogui.hotkey("ctrl", "f10")
  time.sleep(1)
  click_close_record_list()

def stop_record_stream():
  click_window_right_top()
  pyautogui.press("q")

def launch_player():
  click_window_right_top()
  pyautogui.hotkey("ctrl", "c")

  global app_package
  convert_video_command = "launch_player {}".format(app_package)
  pyautogui.write(convert_video_command)
  time.sleep(.1)
  pyautogui.press("enter")

def convert_video():
  click_window_right_top()
  pyautogui.hotkey("ctrl", "c")

  convert_video_command = "convert_video"
  pyautogui.write(convert_video_command)
  time.sleep(.1)
  pyautogui.press("enter")

def shutdown_player():
  shutdown_player_command = "mm api -v 0 shutdown_player"
  os.popen(shutdown_player_command)

def initCount():
  global idList
  global last_count
  last_count = 0
  global last_time
  last_time = round(time.time())
  global maxCount
  randomCount = random.randint(-10 * 1000, 10 * 1000)
  maxCount = 170 * 1000 + randomCount

  if not isListOpen():
    openList()

  global chat_room_id
  checkId(chat_room_id)

def checkId(id):
  clickEnter()

  search(id)
  time.sleep(3)

  if not exists():
    print("{} not exists".format(id))
    
def clickEnter():
  pyautogui.moveTo(1024, 728)
  time.sleep(.1)
  pyautogui.click(1024, 728)

def search(id):
  selectAll()
  time.sleep(.1)
  header = 'live:users:count:'
  pyautogui.write("{}{}".format(header, id))
  time.sleep(.1)
  pyautogui.press('enter')  

def exists():
  pyautogui.moveTo(996, 835)
  time.sleep(.1)
  pixel = pyautogui.pixel(996, 835)
  if pixel == (231, 231, 231):
    pyautogui.click(996, 835)
    return getSelectedCount() > 0
  else:
    print("no data")
    return False

def getSelectedCount():
  clickInput()
  time.sleep(.1)
  refreshCount()
  time.sleep(2)
  clickInput()
    
  selectAll()
  time.sleep(.1)
  
  if not isListOpen() or is_stream_end():
    return
  copySelected()
  selected = clipboard.paste()     
  return stringToInt(selected)

def stringToInt(value):
  try:
    result = int(value)
    return result
  except:
    return 0

def isListOpen():
  time.sleep(.1)
  pixel = pyautogui.pixel(1122, 1039)
  return pixel == (245, 108, 108)

def openList():
  pyautogui.click(1048, 652)
  time.sleep(.1)

def clickInput():
  pyautogui.moveTo(1600, 820)
  time.sleep(.1)
  pyautogui.click(1600, 820)

def refreshCount():
  pyautogui.hotkey("ctrl", "r")

def updateCount():
  global last_count
  global last_time
  
  time.sleep(.1)
  
  clickInput()
  time.sleep(.1)
  refreshCount()
  time.sleep(2)

  clickInput()
  time.sleep(.1)
  selectAll()
  time.sleep(.1)
  
  if not isListOpen() or is_stream_end():
    return
  copySelected()

  try:
      current = int(clipboard.paste())
  except:
      print("selected count error")

  global maxCount
  if current <= 0 or current > maxCount:
      time.sleep(.1)
  elif current - last_count > 3000:
      last_count = current
      if not isListOpen() or is_stream_end():
        return
      time.sleep(10)
  else:
      if current < 10 * 1000:
        add = random.randint(800, 1200)
      elif current > 120 * 1000:
        duration = random.randint(2, 4)
        time.sleep(duration)
        add = random.randint(600, 1000)
      else:
        duration = random.randint(1, 3)
        time.sleep(duration)
        add = random.randint(800, 1200)
      current += add
      clickInput()
      time.sleep(.1)
      selectAll()
      time.sleep(.1)
      pyautogui.write(str(current))

      time.sleep(.1)
      if not isListOpen() or is_stream_end():
        return
      save()
      now = round(time.time())
      print_with_datetime("(+{}) {}(+{})".format(now - last_time, current, add))
      last_time = now
      last_count = current 

def selectAll():
  pyautogui.hotkey("ctrl", "a")

def copySelected():
  pyautogui.hotkey("ctrl", "c")

def save():
  pyautogui.hotkey("ctrl", "s")

def print_with_datetime(text):
  print(datetime.now(), text)

if __name__=="__main__":
  try:
    init()
  except:
    print_with_datetime("-cancel")