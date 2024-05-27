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

def test():
  print('test')

  url = 'https://www.baidu.com'
  result = requests.get(url)
  print(result, result.status_code)

if __name__=="__main__":
  test()
  
  