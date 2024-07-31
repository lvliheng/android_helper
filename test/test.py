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
  time.sleep(3)
  test_command = "adb devices"
  pyautogui.write(test_command)
  pyautogui.press("enter")

if __name__=="__main__":
  test()