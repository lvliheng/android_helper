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
  global app_package
  parser = argparse.ArgumentParser()
  parser.add_argument("-p", "--package", help = "package name")

  args = parser.parse_args()
  if args.package != None:
    app_package = args.package
  else:
    app_package = ""

  print("test: is_app_running: ", is_app_running())

def is_player_started():
  player_state_command = "mm api -v 0 player_state"
  player_state = os.popen(player_state_command).readlines()
  if len(player_state) > 0:
    result = player_state[len(player_state) - 1]
    if "state=start_finished" in result:
      return True
    else:
      return False
  else:
    return False

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


if __name__=="__main__":
  test()