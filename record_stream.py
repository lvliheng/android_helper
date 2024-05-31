from datetime import datetime, timedelta
import pyautogui
import time
import clipboard
import schedule
from pathlib import Path

def init():
  global stream_refresh_hour
  stream_refresh_hour = 1
  global stream_duration_minute
  stream_duration_minute = 30

  start_hour = 19
  start_minute = 30
  global current
  current = datetime.now()
  start_date_time = datetime(current.year, current.month, current.day, start_hour, start_minute)
  end_date_time = datetime(current.year, current.month, current.day, start_hour + stream_refresh_hour, start_minute)
  
  if (current > start_date_time and current < end_date_time):
    start()
  else:
    start_job(start_hour, start_minute)

def start_job(start_hour, start_minute):
  start_task_time = f"{start_hour:02d}:{start_minute:02d}"
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
  check_stream()
  print(f"------------{today}------------")

def check_stream():
  while True:
    if (is_stream_start()):
      start_record()
      break
    elif (is_stream_end()):
      stop_record()

      if (is_after_stream_dead_line()):
        break
      else:
        time.sleep(3)
        pyautogui.moveTo(430, 200)
        pyautogui.dragTo(430, 300, 1, button = "left")
        time.sleep(7)
    elif (is_stream_empty()):
      if (is_after_stream_dead_line()):
        break
      else:
        print_with_datetime("refresh")
        pyautogui.click(470, 300)
        time.sleep(3)
        if (is_stream_start()):
          start_record()
          break
        else:
          time.sleep(7)
    else:
      time.sleep(1)

def is_after_stream_dead_line():
  global stream_dead_line    
  return datetime.now() > stream_dead_line

def is_stream_empty():
  pixel = pyautogui.pixel(470, 300)
  return pixel == (81, 82, 255)

def is_stream_start():
  pixel = pyautogui.pixel(420, 120)
  return pixel == (255, 255, 255)

def is_stream_end():
  pixel = pyautogui.pixel(450, 300)
  return pixel == (81, 82, 255)

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

  pyautogui.click(420, 120)

  global fail_time
  fail_time = 0
  check_stream_url()

  time.sleep(10)
  check_stream()

def check_stream_url():
  stream_url = clipboard.paste()
  if (stream_url.startswith("rtmp:")):
    start_record_screen()
    time.sleep(2)
    start_record_stream(stream_url)
  else:
    global fail_time
    fail_time += 1
    if (fail_time > 5):
      print_with_datetime("invalid")
    else:
      time.sleep(3)
      check_stream_url()

def start_record_screen():
  pyautogui.click(50, 560)
  pyautogui.hotkey("ctrl", "c")

  global directory
  global today_millis

  record_screen_command = "scrcpy -s d1bfafc4 --no-playback --record {}\{}-screen.mp4".format(directory, today_millis)
  pyautogui.write(record_screen_command)
  pyautogui.press("enter")

def start_record_stream(stream_url):
  pyautogui.click(1000, 20)
  pyautogui.hotkey("ctrl", "c")

  global directory
  global today_millis
  record_stream_command = "ffmpeg -i {} -map 0:v -c copy -map 0:a -c copy -strict -2 {}\{}-stream.mp4".format(stream_url, directory, today_millis)
  pyautogui.write(record_stream_command)
  pyautogui.press("enter")

def stop_record():
  print_with_datetime("---stop")
  stop_record_stream()
  time.sleep(1)
  stop_record_screen()

def stop_record_screen():
  pyautogui.click(50, 560)
  pyautogui.hotkey("ctrl", "c")
  time.sleep(1)
  pyautogui.click(450, 300)

def stop_record_stream():
  pyautogui.click(1000, 20)
  pyautogui.press("q")

def print_with_datetime(text):
  print(datetime.now(), text)

if __name__=="__main__":
  try:
    init()
  except:
    print(datetime.now(), "-cancel")