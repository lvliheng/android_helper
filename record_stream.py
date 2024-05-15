from datetime import datetime, timedelta
import pyautogui
import time
import clipboard
import schedule

def start():
  start_time = "19:30"
  print("task will start at {}".format(start_time))

  schedule.every().day.at(start_time).do(init)

  while True:
    schedule.run_pending()
    time.sleep(1)

def init():
  global stream_start
  stream_start = 0
  global stream_dead_line
  stream_dead_line = datetime.now() + timedelta(hours = 2)

  global file_name
  current = datetime.now()
  global today
  today = "{}-{}-{}".format(current.strftime("%Y"), current.strftime("%m"), current.strftime("%d"))
  today_millis = "{}-{}".format(today, current.strftime("%f"))
  file_name = "C:\\Users\\admin\\Downloads\\{}.mp4".format(today_millis)

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
        time.sleep(20)
    elif (is_stream_empty()):
      if (is_after_stream_dead_line()):
        break
      else:
        print(datetime.now(), "refresh")
        pyautogui.click(430, 640)
        time.sleep(2)
        if (is_stream_start()):
          start_record()
          break
        else:
          time.sleep(8)
    else:
      time.sleep(1)

def is_after_stream_dead_line():
  global stream_dead_line    
  return datetime.now() > stream_dead_line

def is_stream_empty():
  pixel = pyautogui.pixel(430, 640)
  return pixel == (80, 82, 255)

def is_stream_start():
  pixel = pyautogui.pixel(240, 240)
  return pixel == (255, 255, 255)

def is_stream_end():
  pixel = pyautogui.pixel(300, 600)
  return pixel == (80, 82, 255)

def start_record():
  print(datetime.now(), "--start")

  global stream_start
  stream_start = datetime.now()
  global stream_dead_line
  stream_dead_line = stream_start + timedelta(minutes = 30)

  start_record_screen()
  time.sleep(2)
  start_record_stream()

def start_record_screen():
  pyautogui.click(240, 240)
  pyautogui.press("F10")

def start_record_stream():
  pyautogui.click(1000, 20)
  pyautogui.hotkey("ctrl", "c")

  global fail_time
  fail_time = 0

  check_stream_url()

def check_stream_url():
  stream_url = clipboard.paste()
  if (stream_url.startswith("rtmp:")):
    do_start_record(stream_url)
  else:
    global fail_time
    fail_time += 1
    if (fail_time > 3):
      print(datetime.now(), "invalid")
    else:
      time.sleep(3)
      check_stream_url()

def do_start_record(stream_url):
  global file_name
  record_stream_command = "ffmpeg -i {} {}".format(stream_url, file_name)
  pyautogui.write(record_stream_command)
  pyautogui.press("enter")

  time.sleep(10)
  check_stream()

def stop_record():
  print(datetime.now(), "---stop")
  stop_record_stream()
  time.sleep(1)
  stop_record_screen()

def stop_record_screen():
  pyautogui.click(300, 600)
  pyautogui.press("F10")
  time.sleep(1)
  pyautogui.click(860, 260)

def stop_record_stream():
  pyautogui.click(1000, 20)
  pyautogui.press("q")

if __name__=="__main__":
  try:
    start()
  except:
    print("-cancel")