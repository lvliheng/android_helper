from datetime import datetime, timedelta
import pyautogui
import time
import clipboard
import schedule
from pathlib import Path
import os

def init():
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
  current = datetime.now()
  stream_dead_line = current + timedelta(hours = stream_refresh_hour)
  today = "{}-{}-{}".format(current.strftime("%Y"), current.strftime("%m"), current.strftime("%d"))

  global directory
  directory = "D:\_temp\stream\{}".format(today)
  Path(directory).mkdir(parents = True, exist_ok = True)

  print(f"------------{today}------------")
  clipboard.copy("")
  check_stream_state()
  print(f"------------{today}------------")

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
  first_item_cover_pixel = pyautogui.pixel(420, 120)
  refresh_button_pixel = pyautogui.pixel(455, 325)
  return refresh_button_pixel == (80, 82, 255) or first_item_cover_pixel == (238, 238, 238)

def is_stream_start():
  pixel = pyautogui.pixel(420, 120)
  return pixel == (255, 255, 255)

def is_stream_end():
  pixel = pyautogui.pixel(450, 300)
  return pixel == (81, 82, 255)

def refresh():
  first_item_cover_pixel = pyautogui.pixel(420, 120)
  refresh_button_pixel = pyautogui.pixel(455, 325)
  if refresh_button_pixel == (80, 82, 255):
    click_refresh()
  elif first_item_cover_pixel == (238, 238, 238):
    drag_refresh()
  else:
    drag_refresh()

def drag_refresh():
  pyautogui.moveTo(430, 200)
  pyautogui.dragTo(430, 300, 1, button = "left")

def click_refresh():
  pyautogui.click(470, 300)

def click_start():
  pyautogui.moveTo(420, 120)
  time.sleep(1)
  pyautogui.click(420, 120)

def click_window_left_bottom():
  pyautogui.click(50, 560)

def click_stop():
  pyautogui.click(450, 300)

def click_window_right_top():
  pyautogui.click(1000, 20)

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

  global try_times
  try_times = 0
  time.sleep(2)
  check_stream_url()

  time.sleep(10)
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
  click_window_left_bottom()
  pyautogui.hotkey("ctrl", "c")

  global directory
  global today_millis

  record_screen_command = "scrcpy -s d1bfafc4 --no-playback --record {}\{}-screen.mp4".format(directory, today_millis)
  pyautogui.write(record_screen_command)
  pyautogui.press("enter")

def start_record_stream(stream_url):
  click_window_right_top()
  pyautogui.hotkey("ctrl", "c")

  global directory
  global today_millis

  record_stream_command = "ffmpeg -y -i {} -map 0:v -c copy -map 0:a -c copy -strict -2 {}\{}-stream.mp4".format(stream_url, directory, today_millis)
  pyautogui.write(record_stream_command)
  pyautogui.press("enter")

def check_file():
  global try_times
  if not is_record_file_exists("screen"):
    try_times += 1
    if try_times <= 5:
      time.sleep(11)
      start_record_screen()
  elif not is_record_file_exists("stream"):
    try_times += 1
    if try_times <= 5:
      time.sleep(11)
      stream_url = clipboard.paste()
      start_record_stream(stream_url)

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
  click_window_left_bottom()
  pyautogui.hotkey("ctrl", "c")
  time.sleep(1)
  click_stop()

def stop_record_stream():
  click_window_right_top()
  pyautogui.press("q")

def print_with_datetime(text):
  print(datetime.now(), text)

if __name__=="__main__":
  init()