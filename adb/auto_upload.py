import os
import time
import random
import pyautogui
import argparse
import screeninfo
import clipboard

def convertLocation(value, isWidth):
  if isWidth == True:
    newValue = (value / monitorWidth) * androidDensity * androidWidth / 100
  else:
    newValue = (value / monitorHeight) * androidHeight
  return newValue

def getPicTap(pic, device, picRegion):
  try:
    location = pyautogui.locateOnScreen(pic, confidence=0.7, region=picRegion, grayscale=True)
    point = pyautogui.center(location)
    x, y = point
    return "adb -s {} shell input tap {} {}".format(device, convertLocation(x, True), convertLocation(y, False))
  except:
    return None

def start(device):
  while True:
    time.sleep(random.randint(3, 5))
    isThirdAppExists = getPicTap('images/third-app.jpg', device, (0, 700, 500, 300))
    if isThirdAppExists != None:
      ignore(device)
      continue
    isBuyExists = getPicTap('images/buy.jpg', device, (0, 700, 500, 300))
    if isBuyExists != None:
      ignore(device)
      continue

    shareTap = getPicTap('images/share.jpg', device, (380, 400, 100, 600))
    if shareTap == None:
      if retryTimes >= 4:
        print("share button not found")
      break
    os.system(shareTap)

    time.sleep(random.randint(1, 2))
    isForwardExists = getPicTap('images/forward.jpg', device, (0, 700, 500, 300))
    if isForwardExists == None:
      ignore(device)
      continue
    
    copyTap = getPicTap('images/copy.jpg', device, (0, 700, 500, 300))
    if copyTap == None:
      copyTap = getPicTap('images/copy1.jpg', device, (0, 700, 500, 300))
      if copyTap == None:
        if retryTimes >= 4:
          print("copy button not found")
        break
    os.system(copyTap)

    time.sleep(random.randint(1, 2))
    uploadTap = "adb -s {} shell input tap 40 120".format(device)
    os.system(uploadTap)

    global index
    index += 1
    print(f" {index}: ", clipboard.paste())

    time.sleep(random.randint(1, 2))
    slide = "adb -s {} shell input swipe 500 800 500 300".format(device)
    os.system(slide)

def ignore(device):
  centerTap = "adb -s {} shell input tap {} {}".format(device, convertLocation(250, True), convertLocation(500, False))
  os.system(centerTap)

  time.sleep(random.randint(1, 2))
  slide = "adb -s {} shell input swipe 500 800 500 300".format(device)
  os.system(slide)

def init(device):
  global androidWidth
  global androidHeight
  global androidDensity
  global monitorWidth
  global monitorHeight
  global index
  index = 0

  sizeCommand = "adb -s {} shell wm size".format(device)
  size = os.popen(sizeCommand).readline()
  androidWidth = int(size[15: -6])
  androidHeight = int(size[-5:])

  densityCommand = "adb -s {} shell wm density".format(device)
  androidDensity = int(os.popen(densityCommand).readline()[-4:])
  # androidDensity = max(androidDensity, 400)
  androidDensity = 400

  monitors = screeninfo.get_monitors()
  monitorWidth = int(monitors[0].width)
  monitorHeight = int(monitors[0].height)

  global retryTimes
  retryTimes = 0

  while retryTimes < 5:
    start(device)
    if retryTimes == 0:
      centerTap = "adb -s {} shell input tap {} {}".format(device, convertLocation(250, True), convertLocation(500, False))
      os.system(centerTap)
    retryTimes += 1

def checkDevices(selectedDevice):
  connected = os.popen("adb devices").readlines()
  devices = [connected[i][0:-8] for i in range(1, len(connected) - 1)]

  if (len(devices) == 0):
    print("no devices found")
  else:
    if selectedDevice != "":
      if selectedDevice in devices:
        init(selectedDevice)
      else:
        print(selectedDevice + " offline")
    else:
      if (len(devices) == 1):
        init(devices[0])
      else:
        print("please select a device")
        
        for i in range(len(devices)):
          print(f"{i + 1}> ", devices[i])
        
        try:
          inputIndex = int(input())
          if inputIndex > 0 and inputIndex < len(devices) + 1:
            selectedDevice = devices[inputIndex - 1]
            checkDevices(selectedDevice)
          else:
            print("selected device is not exist")
        except:
            None

def checkArgs():
  selectedDevice = ""

  parser = argparse.ArgumentParser()
  parser.add_argument("-s", "--select", help = "select device")

  args = parser.parse_args()
  if args.select != None:
      selectedDevice = args.select

  checkDevices(selectedDevice)

if __name__=="__main__":
  try:
    checkArgs()
  except:
    None
