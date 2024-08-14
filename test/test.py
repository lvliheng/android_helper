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
  
  jsonString = '{"a": "123"}'
  # print(jsonString, type(jsonString), len(jsonString))
  
  fileWrite(jsonString)
  fileContent = fileRead()
  # print(fileContent, type(fileContent), len(fileContent))
  
  # result = parseJson(jsonString, "a")
  # print("result", result)
  result2 = parseJson(fileContent, "a")
  print("result2", result2)
  
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