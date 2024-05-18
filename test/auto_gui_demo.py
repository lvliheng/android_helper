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
  x, y = pyautogui.locateCenterOnScreen('images/share.jpg', region=(0, 0, 450, 1200))
  print(x)
  print(y)

def testMouseInfo():
  print('testMouseInfo')
  all = pyautogui.locateAllOnScreen('images/share.jpg')
  print(list(all))

def testscreen():
  print("testscreen")
  # screenshot = pyautogui.screenshot('screen-shot.png')
  screenshot = pyautogui.screenshot('screen-shot.png', region=(50, 560, 400, 400))
  # screenshot = pyautogui.screenshot('screen-shot.png', region=(380, 400, 100, 600))
  screenshot.show()

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

  buttonClick('images/third-app.jpg', (0, 760, 500, 300))

def testPixel():
  pixel = pyautogui.pixel(470, 300)
  print(pixel)
  print(pixel[0], pixel[1], pixel[2])

def testDrag():
  pyautogui.moveTo(430, 200)
  pyautogui.dragTo(430, 500, 1, button="left")

def testClick():
  pyautogui.click(1300, 20)

if __name__=="__main__":
  testscreen()
  # autoClick()
  # testPixel()
  # testDrag()
  # testClick()