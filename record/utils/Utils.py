from datetime import datetime
import pyautogui
import time

def disable_fail_safe():
  pyautogui.FAILSAFE = False

def move_to_safely(x, y):
  try:
    pyautogui.moveTo(x, y)
    time.sleep(.1)
  except:
    time.sleep(1)
    move_to_safely(x, y)

def click_safely(x, y):
  try:
    pyautogui.moveTo(x, y)
    time.sleep(.1)
    pyautogui.click(x, y)
  except:
    time.sleep(1)
    click_safely(x, y)

def drag_to_safely(from_x, from_y, to_x, to_y):
  try:
    pyautogui.moveTo(from_x, from_y)
    time.sleep(.1)
    pyautogui.dragTo(to_x, to_y, 1, button = "left")
  except:
    time.sleep(1)
    drag_to_safely(from_x, from_y, to_x, to_y)

def hot_key_safely(args):
  try:
    pyautogui.hotkey(args)
  except:
    time.sleep(1)
    hot_key_safely(args)

def press_safely(key):
  try:
    pyautogui.press(key)
    return True
  except:
    return False

def write_safely(content, key):
  try:
    pyautogui.write(content)
    time.sleep(.1)
    if not key == "":
      pyautogui.press(key)
    return True
  except:
    return False

def get_pixel_safely(x, y):
  try:
    pixel = pyautogui.pixel(x, y)
    return pixel
  except Exception as e:
    print_with_datetime("get pixel: error:\n{}".format(e))
    time.sleep(1)
    get_pixel_safely(x, y)
   

def print_with_datetime(text):
  print(datetime.now(), text)