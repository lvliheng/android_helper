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


def test():
  print("test")
  

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
  
  fileWrite(jsonString)
  fileContent = fileRead()
  # print(fileContent, type(fileContent), len(fileContent))
  
  # result = parseJson(jsonString, "a")
  # print("result", result)
  result2 = parseJson(fileContent, "a")
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


def fileWrite(content):
  # f = open("config", "a")
  f = open("live_config", "w")
  f.write(content)
  f.close()

def fileRead():
  f = open("live_config", "r")
  return f.read()

def parseJson(jsonString, key):
  value = json.loads(jsonString)
  return value[key]

if __name__=="__main__":
  test()
  # test2()
  # test3()
  # test4()