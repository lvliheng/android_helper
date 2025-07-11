import os
import argparse

def start(device):
  scrcpy = "scrcpy -s {} -Sw --always-on-top --power-off-on-close --window-x=1467 --window-y=60".format(device)
  os.system(scrcpy)

def checkDevices(selectedDevice):
  connected = os.popen("adb devices").readlines()
  devices = [connected[i][0:-8] for i in range(1, len(connected) - 1)]

  if len(devices) == 0:
    print("no devices found")
  else:
    if selectedDevice != "":
      if selectedDevice in devices:
        start(selectedDevice)
      else:
        print(selectedDevice + " not found")
    else:
      if len(devices) == 1:
        start(devices[0])
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
  checkArgs()
  