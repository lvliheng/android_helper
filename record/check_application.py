import os
import time
import argparse

from utils import Utils

def init():
  global application_name
  global application_path

  parser = argparse.ArgumentParser()
  parser.add_argument("-n", "--name", help = "application name")
  parser.add_argument("-p", "--path", help = "application path")

  args = parser.parse_args()
  if args.name != None:
    application_name = args.name
  else:
    application_name = ""
  if args.path != None:
    application_path = args.path
  else:
    application_path = ""

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
  check_application()

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
        Utils.print_with_datetime("--ready: {}".format(check_player_position()))
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

def check_player_position():
  pixel = Utils.get_pixel_safely(28, 23)
  time.sleep(.1)
  return pixel == (15, 154, 255)

def check_application():
  global application_name
  global application_path
  
  command = "tasklist | findstr \"{}\"".format(application_name)
  process_list = os.popen(command).readlines()
  if len(process_list) == 0:
    Utils.hot_key_safely(["win", "r"])
    time.sleep(.1)
    Utils.write_safely("\"{}\{}\"".format(application_path, application_name), "enter")
    time.sleep(5)
  Utils.print_with_datetime("running: {}".format(check_application_position()))

def check_application_position():
  pixel = Utils.get_pixel_safely(1135, 585)
  time.sleep(.1)
  return pixel == (236, 245, 255)

def click_window_left_top():
  time.sleep(.1)
  Utils.click_safely(600, 20) 

if __name__=="__main__":
  init()