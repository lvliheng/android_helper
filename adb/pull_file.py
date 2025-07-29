import os
import argparse

def start(selectedDevice, selectedFilter, selectedRemotePath, selectedLocalPath):
  if selectedFilter == "":
    pull_command = "adb -s {} pull {} {}".format(selectedDevice, selectedRemotePath, selectedLocalPath)
    os.system(pull_command)
  else:
    ls_command = "adb -s {} shell \"ls -R {} | grep {}\"".format(selectedDevice, selectedRemotePath, selectedFilter)
    file_names = os.popen(ls_command).readlines()
    for file_name in file_names:
      pull_command = "adb -s {} pull {}{} {}".format(selectedDevice, selectedRemotePath, file_name.strip(), selectedLocalPath)
      os.system(pull_command)

def checkDevices(selectedDevice, selectedFilter, selectedRemotePath, selectedLocalPath):
  connected = os.popen("adb devices").readlines()
  devices = [connected[i][0:-8] for i in range(1, len(connected) - 1)]

  if len(devices) == 0:
    print("no devices found")
  else:
    if selectedDevice != "":
      if selectedDevice in devices:
        start(selectedDevice, selectedFilter, selectedRemotePath, selectedLocalPath)
      else:
        print(selectedDevice + " not found")
    else:
      if len(devices) == 1:
        start(devices[0], selectedFilter, selectedRemotePath, selectedLocalPath)
      else:
        print("please select a device")
        
        for i in range(len(devices)):
          print(f"{i + 1}> ", devices[i])
        
        try:
          inputIndex = int(input())
          if inputIndex > 0 and inputIndex < len(devices) + 1:
            selectedDevice = devices[inputIndex - 1]
            checkDevices(selectedDevice, selectedFilter, selectedRemotePath, selectedLocalPath)
          else:
            print("selected device is not exist")
        except:
            None

def checkArgs():
  selectedDevice = ""
  selectedFilter = ""
  selectedRemotePath = "/sdcard/Pictures/Screenshots/"
  selectedLocalPath = ""
  
  parser = argparse.ArgumentParser()
  parser.add_argument("-s", "--select", help = "select device")
  parser.add_argument("-f", "--filter", help = "file name filter")
  parser.add_argument("-r", "--remote", help = "android sdcard directory path(default is '/sdcard/Pictures/Screenshots/')")
  parser.add_argument("-l", "--local", help = "pc directory path")

  args = parser.parse_args()
  if args.select != None:
    selectedDevice = args.select
  if args.filter != None:
    selectedFilter = args.filter
  if args.remote != None:
    selectedRemotePath = args.remote
  if args.local != None:
    selectedLocalPath = args.local
  if selectedLocalPath == "-1":
    selectedLocalPath = ""

  checkDevices(selectedDevice, selectedFilter, selectedRemotePath, selectedLocalPath)

if __name__=="__main__":
  checkArgs()