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
import json
import requests
from pynput import keyboard
import base64
import ctypes

import asyncio
import websockets

def test():
  print("test")
  
  while True:
    time.sleep(3)
    get_pixel(1360, 606)

def getPixel(x, y):
  try:
    pixel = pyautogui.pixel(x, y)
    print("({}, {}) : {}".format(x, y, pixel))
  except:
    print("pixel: error:")
    time.sleep(3)

def test_exception():
  try:
    count = 0
    while True:
      count += 1
      print(count)
      time.sleep(2)
  except KeyboardInterrupt as e:
    print("test: error:", e)

def test_return():
  while True:
    time.sleep(2)
    
    print("loop start")
    x = random.randint(0, 1)
    if x % 2 == 0:
      test_fun_a()
      
    print("loop end")
    
def test_fun_a():
  print("fun a start")
  x = random.randint(0, 1)
  if x % 2 == 0:
    print("fun a return")
    return
  print("fun a end")
  

def test_condition(a, b):
  result = not a or b
  print(a, b, "==>", result)
  
def test1():  
  jsonString = '{"a": "123"}'
  # print(jsonString, type(jsonString), len(jsonString))
  
  file_write(jsonString)
  fileContent = file_read()
  # print(fileContent, type(fileContent), len(fileContent))
  
  # result = parse_json(jsonString, "a")
  # print("result", result)
  result2 = parse_json(fileContent, "a")
  print("result2", result2)
  

def test2():
  # command = "adb shell \"dumpsys window windows | grep -E 'mCurrentFocus|mFocusedApp'\""
  command = "adb shell \"dumpsys activity activities | grep -E 'mCurrentFocus|mFocusedApp'\""
  print(command)
  os.system(command)

def test3():
  while True:
    random_count = random.randint(9950, 10050)
    duration_string = str(random_count)
    print("duration_string", duration_string)
    duration_lenght = len(duration_string)
    print("duration_lenght before:", duration_lenght)
    if duration_lenght < 5:
      for x in range(5 - duration_lenght):
        duration_string += " "
    duration_lenght_after = len(duration_string)
    print("durationlenght after:", duration_lenght_after)
    if duration_lenght >= 5:
      break

def test4():
  times = 0
  while True:
    times += 1
    if times > 10:
      break
    
    time.sleep(1)
    print(str(datetime.now), str(times))

def test_format(value, max):
  # return format(value, "03")
  
  # return "% 3s" % value
  # return "% 3d" % value
  return "{:<{}}".format(value, max)

def get_string_full_length(value_int, max_length):
  return "{:<{}}".format(value_int, max_length)

def string_to_int(value):
  try:
    result = int(value)
    return result
  except:
    return 0


def file_write(content):
  # f = open("config", "a")
  f = open("live_config", "w")
  f.write(content)
  f.close()

def file_read():
  f = open("live_config", "r")
  return f.read()

def parse_json(jsonString, key):
  value = json.loads(jsonString)
  return value[key]

def check_application():
  command = "tasklist | findstr \"Another Redis Desktop Manager.exe\""
  process_list = os.popen(command).readlines()
  print(process_list)
  if len(process_list) == 0:
    pyautogui.hotkey("win", "r")
    time.sleep(.1)
    pyautogui.write("\"D:\_tools\AnotherRedis\Another Redis Desktop Manager\Another Redis Desktop Manager.exe\"")
    time.sleep(.1)
    pyautogui.press("enter")
  else:
    print("running")

def task_kill():
  task_kill_command = "taskkill /f /im \"Another Redis Desktop Manager.exe\""
  os.system(task_kill_command)
  time.sleep(1)
  check_application()
  
def check():
  check_application_command = "check_application"
  pyautogui.write(check_application_command)
  pyautogui.press("enter")

def test_property():
  a = 1
  test_propery2(a)
  print("test_property:", a)
  
def test_propery2(a):
  a += 1
  print("test_property2:", a)

def test_adb():
  # command = "adb shell \"dumpsys window windows | grep -E 'mCurrentFocus|mFocusedApp'\""
  command = "adb shell \"dumpsys window windows\""
  os.system(command)

def test_keyboard_listener():
  global listener
  listener = keyboard.Listener(on_press=on_press)
  listener.start()
  listener.join()
  
def on_press(key):
  if key == keyboard.Key.esc:
    global listener
    listener.stop()
  elif key == keyboard.Key.enter:
    print("enter")
    get_position()
  else:
    print("on_press:", key)

def get_pixel(x, y):
  pixel = pyautogui.pixel(x, y)
  print("({}, {}) : {}".format(x, y, pixel))
  print("pixel's type:", type(pixel))

def get_position():
  x, y = pyautogui.position()
  positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
  print(positionStr, end='')
  print('\b' * len(positionStr), end='', flush=True)
  get_pixel(x, y)

def test_create_file():
  root = "D:\\_temp\\stream\\"
  action_config_file = "{}{}".format(root, "new_action_config")
  is_exists = Path(action_config_file).exists()
  print("is_exists:", is_exists)
  if not is_exists:
    open(action_config_file, "w")

def test_base64():
  test = "a"
  encode_bytes = base64.b64encode(test.encode("ascii"))
  encode_result = encode_bytes.decode("ascii")
  print(test, " ==> ", encode_result)
  
  decode_bytes = base64.b64decode(encode_result.encode("ascii"))
  decode_result = decode_bytes.decode("ascii")
  print(encode_result, " ==> ", decode_result)

def websockets_start():
  global connections
  connections = set()
  
  asyncio.run(websockets_main())
  
async def websockets_main():
  async with websockets.serve(websockets_echo, "192.168.0.2", 8765):
    await asyncio.Future()

async def websockets_echo(websocket):
  global connections
  if websocket not in connections:
    connections.add(websocket)
    
  async for message in websocket:
    print("websockets_echo: message:", message)
    websockets.broadcast(connections, message)

if __name__=="__main__":
  test()
  # test2()
  # test3()
  # test4()
  # test_exception()
  # check_application()
  # task_kill()
  # test_property()
  # test_adb()
  # test_keyboard_listener()
  # test_create_file()
  # test_base64()
  # websockets_start()
  # get_pixel(372, 555)