import os
import time
import schedule
from datetime import datetime
import pyautogui
from pathlib import Path

def init():
  global app_package
  app_package = ""

  start_hour = 19
  start_minute = 20
  
  start_job(start_hour, start_minute)

def start_job(start_hour, start_minute):
  stream_refresh_hour = 1
  global current
  current = datetime.now()
  start_date_time = datetime(current.year, current.month, current.day, start_hour, start_minute)
  global end_date_time
  end_date_time = datetime(current.year, current.month, current.day, start_hour + stream_refresh_hour, start_minute)
  start_task_time = f"{start_hour:02d}:{start_minute:02d}"

  if current > start_date_time and current < end_date_time:
    check_player_state()
  else:
    print("-----task will start at {}-----".format(start_task_time))
  
  schedule.every().day.at(start_task_time).do(check_player_state)

  while True:
    schedule.run_pending()
    time.sleep(1)

def check_player_state():
  shutdown_player()
  time.sleep(4)

  player_state_command = "mm api -v 0 player_state"

  try_times = 0
  while True:
    if try_times > 5:
      print_with_datetime("player state error")
      break

    time.sleep(10)

    player_state = os.popen(player_state_command).readlines()
    print_with_datetime(player_state)
    
    if (len(player_state) > 0):
      result = player_state[len(player_state) - 1]
      if ("result=-2" in result):
        launch_player()
        try_times += 1
      elif ("state=start_finished" in result):
        print_with_datetime("player start finished")
        click_window_left_top()
        check_app_state()
        break
      else:
        print_with_datetime(result)

def launch_player():
  launch_player_command = "mm api -v 0 launch_player"
  os.system(launch_player_command)

def shutdown_player():
  shutdown_player_command = "mm api -v 0 shutdown_player"
  os.system(shutdown_player_command)

def check_app_state():
  global app_package
  app_state_command = "mm api -v 0 app_state {}".format(app_package)
  
  try_times = 0
  while True:
    if try_times > 5:
      break

    time.sleep(5)

    app_state = os.popen(app_state_command).readlines()
    print_with_datetime(app_state)

    if (len(app_state) > 0):
      result = app_state[len(app_state) - 1]
      if ("result=-2" in result):
        launch_app()
      elif ("state=stopped" in result):
        launch_app()
      elif ("state=running" in result):
        print_with_datetime("app running")
        if check_button():
          print_with_datetime("app ready")

          if is_record_enabled():
            print_with_datetime("record ready")
            break
          else:
            time.sleep(2)
            check_player_state()
            break
        else:
          try_times += 1
          if try_times > 5:
            print_with_datetime("app state error")
            break
      else:
        print_with_datetime(result)

def launch_app():
  global app_package
  launch_app_command = "mm api -v 0 launch_app {}".format(app_package)
  os.system(launch_app_command)

def close_app():
  global app_package
  close_app_command = "mm api -v 0 close_app {}".format(app_package)
  os.system(close_app_command)

def check_button():
  try_times = 0
  is_succeed = False
  while True:
    time.sleep(2)

    yellow_pixel = pyautogui.pixel(712, 910)
    yellow_exist = yellow_pixel == (222, 197, 69)
    white_pixel = pyautogui.pixel(222, 972)
    white_exist = white_pixel == (255, 255, 255)
    if yellow_exist and white_exist:
      click_button()
      is_succeed = True
      break
    else:
      try_times += 1
      drag_next()
  return is_succeed

def click_button():
  pyautogui.click(710, 830)

def drag_next():
  pyautogui.moveTo(485, 900)
  pyautogui.dragTo(485, 200, 1, button = "left")

def is_record_enabled():
  len_before = file_list_len()

  start_record_screen()
  time.sleep(5)
  stop_record_screen()
  time.sleep(1)
  click_close_record_list()

  len_after = file_list_len()
  return len_after > len_before

def file_list_len():
  root = "D:\_temp\stream\\"
  record_directory = "{}record".format(root)
  Path(record_directory).mkdir(parents = True, exist_ok = True)
  file_list = os.listdir(record_directory)
  return len(file_list)

def start_record_screen():
  click_window_left_top()
  pyautogui.press("F10")

def click_window_left_top():
  pyautogui.click(640, 20) 

def stop_record_screen():
  pyautogui.hotkey("ctrl", "F10")

def click_close_record_list():
  pyautogui.click(860, 260)

def print_with_datetime(text):
  print(datetime.now(), text)

if __name__=="__main__":
  init()