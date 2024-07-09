import os
import time
import random
import sys
import argparse
import screeninfo
import clipboard
import schedule
from datetime import datetime, timedelta
import platform
from pathlib import Path
import pyautogui
import subprocess
import requests
from PIL import Image

def test():
  print('test')

  test_command = "adb shell \"dumpsys window windows | grep -E 'mCurrentFocus|mFocusedApp'\""
  os.system(test_command)

  global app_package
  app_package = ""
  # check_player_state()
  # check_app_state()
 
def compress():
  input_file = "C:\\Users\\admin\\Desktop\\8.png"
  output_file = "C:\\Users\\admin\\Desktop\\9.png"
  file = Image.open(input_file)
  # file.resize((876, 659))
  file.convert("P", palette=Image.ADAPTIVE, colors=256)
  file.save(output_file, optimize=True, quality=85)
  file.close()

def check_player_state():
  player_state_command = "mm api -v 0 player_state"
  player_state = os.popen(player_state_command).readlines()
  print("player state: ", player_state)
  
  if (len(player_state) > 0):
    result = player_state[len(player_state) - 1]
    if ("result=-2" in result):
      launch_player()
    elif ("state=start_finished" in result):
      print("player start finished")
    else:
      print("player state:", result)

def launch_player():
  print("launch_player")
  launch_player_command = "mm api -v 0 launch_player"
  os.system(launch_player_command)

def shutdown_player():
  shutdown_player_command = "mm api -v 0 shutdown_player"
  os.system(shutdown_player_command)

def check_app_state():
  global app_package
  app_state_command = "mm api -v 0 app_state {}".format(app_package)
  app_state = os.popen(app_state_command).readlines()
  print("app state: ", app_state)

  if (len(app_state) > 0):
    result = app_state[len(app_state) - 1]
    if ("state=stopped" in result):
      launch_app()
    elif ("state=running" in result):
      print("app running")
    else:
      print("app state:", result)

def launch_app():
  global app_package
  launch_app_command = "mm api -v 0 launch_app {}".format(app_package)
  os.system(launch_app_command)

def close_app():
  global app_package
  close_app_command = "mm api -v 0 close_app {}".format(app_package)
  os.system(close_app_command)

if __name__=="__main__":
  # test()
  compress()