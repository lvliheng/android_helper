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
  print("test")
  init()

def init():
  global idList
  idList = ["194293417443329", "177712867115010", "229915271168007"]
  global index
  index = 0

  start(idList[index])

def start(chatRoomId):
  clickEnter()

  search(chatRoomId)
  time.sleep(3)

  if exists():
    clickInput()
    time.sleep(.4)

    refresh()
    time.sleep(2)
    
    clickInput()
    time.sleep(.4)
    inputNewCount()
  else:
    print("chat room {} not exists".format(chatRoomId))
    tryOtherId()

def clickEnter():
  pyautogui.moveTo(1024, 728)
  time.sleep(.4)
  pyautogui.click(1024, 728)

def search(chatRoomId):
  pyautogui.hotkey('ctrl', 'a')
  time.sleep(.4)
  keyword = 'live:users:count:'
  # chatRoomId = '240966941343747'
  # chatRoomId = '229915271168007'
  pyautogui.write("{}{}".format(keyword, chatRoomId))
  time.sleep(.4)
  pyautogui.press('enter')  

def exists():
  pyautogui.moveTo(996, 835)
  time.sleep(.4)
  pixel = pyautogui.pixel(996, 835)
  if pixel == (231, 231, 231):
    pyautogui.click(996, 835)
    return True
  else:
    print("no data")
    return False

def tryOtherId():
  global idList
  global index
  index = len(idList) - idList
  start(idList[index])

def clickInput():
  pyautogui.moveTo(1600, 820)
  time.sleep(.4)
  pyautogui.click(1600, 820)

def refresh():
  pyautogui.hotkey("f5")

def inputNewCount():
  pyautogui.hotkey("ctrl", "a")
  time.sleep(.4)
  pyautogui.write("test")

def save():
  pyautogui.hotkey("ctrl", "s")

if __name__=="__main__":
  test()