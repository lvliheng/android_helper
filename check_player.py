import os
import time
import schedule
from datetime import datetime
import pyautogui

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
  global today
  today = "{}-{}-{}".format(current.strftime("%Y"), current.strftime("%m"), current.strftime("%d"))
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
  global today
  print(f"------------{today}------------")
  check_player_state()
  print(f"------------{today}------------")

def check_player_state():
  shutdown_player()
  time.sleep(10)

  player_state_command = "mm api -v 0 player_state"

  try_times = 0
  while True:
    if try_times > 5:
      print("++++++++player state error++++++++")
      break

    time.sleep(10)

    player_state = os.popen(player_state_command).readlines()
    
    if (len(player_state) > 0):
      result = player_state[len(player_state) - 1]
      if ("result=-2" in result):
        launch_player()
      elif ("state=start_finished" in result):
        click_window_left_top()
        check_app_state()
        break
      else:
        try_times += 1

def launch_player():
  launch_player_command = "mm api -v 0 launch_player"
  os.popen(launch_player_command)

def shutdown_player():
  shutdown_player_command = "mm api -v 0 shutdown_player"
  os.popen(shutdown_player_command)

def check_app_state():
  global app_package
  app_state_command = "mm api -v 0 app_state {}".format(app_package)
  
  try_times = 0
  while True:
    if try_times > 5:
      break

    time.sleep(10)

    app_state = os.popen(app_state_command).readlines()

    if (len(app_state) > 0):
      result = app_state[len(app_state) - 1]
      if ("result=-2" in result):
        launch_app()
      elif ("state=stopped" in result):
        close_app()
        time.sleep(10)
        launch_app()
      elif ("state=running" in result):
        if check_button():
          print_with_datetime("--ready")
          break
        else:
          try_times += 1
          if try_times > 5:
            print("+++++++++button not found+++++++++")
            break

def launch_app():
  global app_package
  launch_app_command = "mm api -v 0 launch_app {}".format(app_package)
  os.popen(launch_app_command)

def close_app():
  global app_package
  close_app_command = "mm api -v 0 close_app {}".format(app_package)
  os.popen(close_app_command)

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

def click_window_left_top():
  pyautogui.click(640, 20) 

def print_with_datetime(text):
  print(datetime.now(), text)

if __name__=="__main__":
  init()