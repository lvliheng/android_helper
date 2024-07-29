import os
import time
from datetime import datetime
import argparse
import pyautogui

def init():
  global app_package

  parser = argparse.ArgumentParser()
  parser.add_argument("-p", "--package", help = "package name")

  args = parser.parse_args()
  if args.package != None:
    app_package = args.package
  else:
    app_package = ""

  start()

def start():
  pyautogui.hotkey("ctrl", "win", "left")
  time.sleep(1)
  pyautogui.hotkey("ctrl", "win", "left")
  time.sleep(1)
  click_window_left_top()
  time.sleep(1)

  check_player_state()

def check_player_state():
  shutdown_player()
  time.sleep(10)

  player_state_command = "mm api -v 0 player_state"

  try_times = 0
  while True:
    if try_times > 5:
      print("++++++++player state error++++++++")
      break

    time.sleep(20)

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

  if app_package == "":
    return

  app_state_command = "mm api -v 0 app_state {}".format(app_package)
  
  try_times = 0
  while True:
    if try_times > 5:
      break

    time.sleep(20)

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

    yellow_pixel = pyautogui.pixel(910, 915)
    yellow_exist = yellow_pixel == (222, 197, 69)
    white_pixel = pyautogui.pixel(458, 964)
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
  pyautogui.click(910, 850)

def drag_next():
  pyautogui.moveTo(485, 900)
  pyautogui.dragTo(485, 200, 1, button = "left")

def click_window_left_top():
  pyautogui.click(600, 20) 

def print_with_datetime(text):
  print(datetime.now(), text)

if __name__=="__main__":
  init()