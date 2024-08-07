from datetime import datetime, timedelta
import pyautogui
import time
import clipboard
import schedule
from pathlib import Path
import os
import argparse

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
  first_item_cover_pixel = pyautogui.pixel(320, 220)
  refresh_button_pixel = pyautogui.pixel(430, 640)
  return (refresh_button_pixel == (199, 7, 22) or first_item_cover_pixel == (238, 238, 238))

def is_stream_start():
  pixel = pyautogui.pixel(320, 220)
  return pixel == (255, 255, 255)

def is_stream_end():
  pixel = pyautogui.pixel(330, 620)
  return pixel == (199, 7, 22)

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
  first_item_cover_pixel = pyautogui.pixel(320, 220)
  refresh_button_pixel = pyautogui.pixel(430, 640)
  if refresh_button_pixel == (199, 7, 22):
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
  time.sleep(1)
  pyautogui.click(320, 220)

def click_window_left_top():
  pyautogui.click(600, 20)

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

  time.sleep(30)
  global try_times
  if not is_stream_end():
    try_times = 0
    check_stream_url()    

  time.sleep(10)
  try_times = 0
  check_stream_state()

def check_stream_url():
  stream_url = clipboard.paste()
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

def is_record_file_exists(type):
  global directory
  global today_millis
  record_file = Path("{}\{}-{}.mp4".format(directory, today_millis, type))
  return record_file.is_file() and os.path.getsize(record_file) > 0

def stop_record():
  print_with_datetime("---stop")

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
  pyautogui.press("enter")

def convert_video():
  click_window_right_top()
  pyautogui.hotkey("ctrl", "c")

  convert_video_command = "convert_video"
  pyautogui.write(convert_video_command)
  pyautogui.press("enter")

def shutdown_player():
  shutdown_player_command = "mm api -v 0 shutdown_player"
  os.popen(shutdown_player_command)

def print_with_datetime(text):
  print(datetime.now(), text)

if __name__=="__main__":
  init()
  # try:
  #   init()
  # except:
  #   print_with_datetime("-cancel")