import pyautogui
import time
import clipboard
import random
from datetime import datetime

def init():
  global idList
  idList = ["194293417443329", "177712867115010", "229915271168007"]
  global index
  index = 0

  if not isListOpen():
    openList()

  start(idList[index])

def start(chatRoomId):
  print("start:", chatRoomId)
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
  header = 'live:users:count:'
  pyautogui.write("{}{}".format(header, chatRoomId))
  time.sleep(.4)
  pyautogui.press('enter')  

def exists():
  pyautogui.moveTo(996, 835)
  time.sleep(.4)
  pixel = pyautogui.pixel(996, 835)
  if pixel == (231, 231, 231):
    pyautogui.click(996, 835)
    return isCountValid()
  else:
    print("no data")
    return False

def isCountValid():
  try_times = 0
  is_valid = False
  while True:
    if getSelectedCount() > 0:
      is_valid = True
      break
    else:
      try_times += 1
      if try_times > 3:
        break
  return is_valid

def getSelectedCount():
  clickInput()
  time.sleep(.4)
  refresh()
  time.sleep(2)
  clickInput()
    
  pyautogui.hotkey("ctrl", "a")
  time.sleep(.4)
  pyautogui.hotkey("ctrl", "c")
  selected = clipboard.paste()     
  return stringToInt(selected)

def stringToInt(value):
  try:
    result = int(value)
    return result
  except:
    return 0

def tryOtherId():
  global idList
  global index
  index += 1
  if index < len(idList):
    start(idList[index])
  else:
    print("no chat room id valid")

def isListOpen():
  pixel = pyautogui.pixel(1122, 1039)
  return pixel == (245, 108, 108)

def openList():
  pyautogui.click(1048, 652)
  time.sleep(.4)

def clickInput():
  pyautogui.moveTo(1600, 820)
  time.sleep(.4)
  pyautogui.click(1600, 820)

def refresh():
  pyautogui.hotkey("ctrl", "r")

def inputNewCount():
  last = 0
  start = round(time.time())

  while True:
      #refresh
      duration = random.randint(5, 8)
      # duration = random.randint(5, 10)
      time.sleep(duration)
      pyautogui.click(1200, 300)
      pyautogui.hotkey("ctrl", "r")
      time.sleep(2)

      #focus
      pyautogui.click(1200, 300)
      time.sleep(.2)
      pyautogui.hotkey("command", "a")
      time.sleep(.2)
      pyautogui.hotkey("command", "c")

      try:
          current = int(clipboard.paste())
      except:
          break

      count = random.randint(-5000, 5000)
      max = 160000 + count
      if current <= 0 or current > max:
          break
      elif current - last > 3000:
          last = current
          time.sleep(.2)
      else :
          add = random.randint(800, 1200)
          # add = random.randint(500, 1000)
          current += add
          pyautogui.click(1200, 300)
          pyautogui.hotkey("command", "a")
          time.sleep(.2)
          pyautogui.write(str(current))

          time.sleep(.2)
          save()
          now = round(time.time())
          print("{}(+{}): {}(+{})".format(datetime.now(), now - start, current, add))
          start = now
          last = current

def save():
  pyautogui.hotkey("ctrl", "s")

if __name__=="__main__":
    init()