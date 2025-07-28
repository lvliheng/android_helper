import os
import time
import argparse
import pygetwindow as gw

from utils import Utils

def init():
  global application_name
  global application_path
  global title_application
  global title_player

  parser = argparse.ArgumentParser()
  parser.add_argument("-n", "--name", help = "application name")
  parser.add_argument("-p", "--path", help = "application path")
  parser.add_argument("-ta", "--titleapplication", help = "application window title")
  parser.add_argument("-tp", "--titleplayer", help = "player window title")

  args = parser.parse_args()
  if args.name != None:
    application_name = args.name
  else:
    application_name = ""
  if args.path != None:
    application_path = args.path
  else:
    application_path = ""
  if args.titleapplication != None:
    title_application = args.titleapplication
  else:
    title_application = ""
  if args.titleplayer != None:
    title_player = args.titleplayer
  else:
    title_player = ""

  start()
  
def start():
  time.sleep(3)
  Utils.hot_key_safely(["ctrl", "win", "left"])
  time.sleep(1)
  Utils.hot_key_safely(["ctrl", "win", "left"])
  time.sleep(1)
  click_window_left_top()
  time.sleep(1)

  check_player()
  time.sleep(2)
  check_application()
  check_window()

def check_player():
  player_state_command = "mm api -v 0 player_state"

  try_times = 0
  while True:
    if try_times > 5:
      print("++++++++player state error++++++++")
      break

    player_state = os.popen(player_state_command).readlines()

    if (len(player_state) > 0):
      result = player_state[len(player_state) - 1]
      if ("result=-2" in result):
        launch_player()
      elif ("state=start_finished" in result):
        if is_player_error():
          shutdown_player()
          time.sleep(2)
          check_player()
        break
      else:
        try_times += 1

    time.sleep(15)

def launch_player():
  launch_player_command = "mm api -v 0 launch_player"
  os.popen(launch_player_command)

def shutdown_player():
  shutdown_player_command = "mm api -v 0 shutdown_player"
  os.popen(shutdown_player_command)

def is_player_error():
  red_icon_pixel = Utils.is_pixel_match_color_safely(406, 597, (0, 209, 255))
  time.sleep(.1)
  restart_button_pixel = Utils.is_pixel_match_color_safely(284, 484, (255, 0, 104))
  time.sleep(.1)
  return red_icon_pixel and restart_button_pixel

def check_application():
  global application_name
  global application_path
  
  filter_name = application_name[:21]
  command = "tasklist | findstr \"{}\"".format(filter_name)
  process_list = os.popen(command).readlines()
  if len(process_list) == 0:
    Utils.hot_key_safely(["win", "r"])
    time.sleep(.1)
    Utils.write_safely("\"{}\{}\"".format(application_path, application_name), "enter")
    time.sleep(5)

def check_window():
  global title_application
  global title_player
  for window in gw.getAllWindows():
    if window.title == title_application:
      window.activate()
      time.sleep(1)
      window.moveTo(953, 540)
      window.resizeTo(974, 547)
      time.sleep(1)
    elif window.title == title_player:
      window.activate()
      time.sleep(1)
      window.moveTo(-3, 0)
      window.resizeTo(966, 1083)
      time.sleep(1)

def select_all():
  Utils.hot_key_safely(["ctrl", "a"])

def task_kill():
  task_kill_command = "taskkill /f /im \"{}\"".format(application_name)
  os.system(task_kill_command)

def click_window_left_top():
  time.sleep(.1)
  Utils.click_safely(500, 20)
  
if __name__=="__main__":
  init()