import pyautogui
import time

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
  pyautogui.moveTo(485, 900)
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
  screenshot = pyautogui.screenshot('screen-shot.png', region=(910, 850, 400, 400))
  # screenshot = pyautogui.screenshot('screen-shot.png', region=(380, 400, 100, 600))
  screenshot.show()


def testPixel():
  pixel = pyautogui.pixel(910, 915)
  print(pixel)
  print(pixel[0], pixel[1], pixel[2])

if __name__=="__main__":
  testscreen()
  # testPixel()
  # autoClick()
  # testDrag()
  # testClick()