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
  pyautogui.hotkey("command", "s")

if __name__=="__main__":
    init()