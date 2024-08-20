import pyautogui
import time
import random

def testLocateOnScreen():
  print('testLocateOnScreen')
  # sharelocation = pyautogui.locateOnScreen('images/share.jpg', confidence=0.5, region=(0, 0, 450, 1200))
  sharelocation = pyautogui.locateOnScreen('images/share.jpg', confidence=0.5, region=(0, 0, 450, 1200))
  # sharelocation = pyautogui.locateOnScreen('images/share.jpg', grayscale=True)
  print(sharelocation)
  sharepoint = pyautogui.center(sharelocation)
  print(sharepoint)
  sharex, sharey = sharepoint
  print(sharex, sharey)
  # pyautogui.click(sharex, sharey)

def testLocateCenterOnScreen():
  print('testLocateCenterOnScreen')
  # x, y = pyautogui.locateCenterOnScreen('share.jpg', grayscale=True)
  x, y = pyautogui.locateCenterOnScreen('images/heart.png', region=(670, 530, 100, 100))
  print(x)
  print(y)

def testMouseInfo():
  print('testMouseInfo')
  all = pyautogui.locateAllOnScreen('images/share.jpg')
  print(list(all))

def buttonClick(pic, picRegion):
  try:
    # sharelocation = pyautogui.locateOnScreen(pic, confidence=0.7, region=(380, 400, 100, 600))
    sharelocation = pyautogui.locateOnScreen(pic, confidence=0.7, region=picRegion, grayscale=True)
    sharepoint = pyautogui.center(sharelocation)
    sharex, sharey = sharepoint
    print(sharex, sharey)
    pyautogui.click(sharex, sharey)
  except:
    if pic == 'images/copy.jpg':
      buttonClick('images/copy1.jpg', (0, 700, 500, 300))
    else:
      print(pic, " not found")

def autoClick():
  # print("======shareClick======")
  # buttonClick('images/share.jpg', (380, 400, 100, 600))

  # time.sleep(2)
  # print("======copyClick======")
  # buttonClick('images/copy.jpg', (0, 760, 500, 300))

  # buttonClick('images/third-app.jpg', (0, 760, 500, 300))
  buttonClick('images/yellow.jpg', (685, 885, 60, 60))

def testDrag():
  while True:
    time.sleep(2)
    try:
      pyautogui.moveTo(485, 900)
      time.sleep(.1)
      
    except:
      time.sleep(1)
      testDrag()
    
    time.sleep(2)
    pyautogui.dragTo(485, 200, 1, button = "left")

def testClick():
  pyautogui.click(590, 420)
  
def testHotKey():
  pyautogui.click(450, 300)
  time.sleep(1)
  pyautogui.hotkey("ctrl", "F10")

def testscreen():
  print("testscreen")
  # screenshot = pyautogui.screenshot('screen-shot.png')
  screenshot = pyautogui.screenshot('screen-shot.png', region=(1024, 728, 270, 280))
  # screenshot = pyautogui.screenshot('screen-shot.png', region=(380, 400, 100, 600))
  screenshot.show()


def testPixel():
  while True:
    time.sleep(2)
    
    try:
      pixel = pyautogui.pixel(232, 986)
      print(pixel)
      print(pixel[0], pixel[1], pixel[2])
    except Exception as e:
      print("===test pixel: error:===\n", e)

def testPosition():
  try:
    while True:
        x, y = pyautogui.position()
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        print(positionStr, end='')
        print('\b' * len(positionStr), end='', flush=True)
  except KeyboardInterrupt:
      print('\n')

def test_move_to():
  times = 0
  while True:
    times += 1
    if times > 30:
      break
    
    time.sleep(2)
    try:
      pyautogui.moveTo(1000, 1000)
    except Exception as e:
      print("+++test move to moveTo error:+++\n", e)
    
    time.sleep(.1)
      
    try:
      pyautogui.click(1000, 1000)
    except Exception as e:
      print("---test move to click error:---\n", e)

def test_hot_key():
  while True:
    time.sleep(2)
    # pyautogui.hotkey("ctrl", "win", "left")
    # pyautogui.hotkey(["ctrl", "win", "left"])
    pyautogui.press("1")

def test_write():
  while True:
    time.sleep(2)
    try:
      pyautogui.write("{} ".format(str(random.randint(0, 100))))
    except Exception as e:
      print("test write error: " + e)

if __name__=="__main__":
  # testscreen()
  # testPosition()
  # testPixel()
  # autoClick()
  # testDrag()
  # testClick()
  # test_move_to()
  # test_hot_key()
  test_write()