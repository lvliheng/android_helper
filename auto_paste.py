import os
import time
import random
import pyautogui
import argparse
import screeninfo
import clipboard

def start(device):
  while True:
    time.sleep(0.2)
  
    global lastContent
    currentContent = clipboard.paste()
    if currentContent.startswith("szbbmusic") == False:
      continue
    if currentContent == "" or lastContent == currentContent:
      continue
    lastContent = currentContent
    
    switchWindowFocus()
    pyautogui.hotkey("Ctrl","v")

    time.sleep(0.2)
    global index
    index += 1
    print(f" {index}: ", lastContent)

    time.sleep(0.2)
    uploadTap = "adb -s {} shell input tap 40 120".format(device)
    os.system(uploadTap)

def switchWindowFocus():
  lastX, lastY = pyautogui.position()
  pyautogui.click(200, 40)
  pyautogui.moveTo(lastX, lastY)

def init(device):
  global index
  index = 0
  global lastContent
  lastContent = ""

  start(device)

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
