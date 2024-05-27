import os
import time
import argparse

def start(command):
  try:
    os.system(command)
  except:
    print('check_command: error')
    time.sleep(10)
    start(command)
    
def checkArgs():
  args_command = ""
  remote = ""
  local = ""

  parser = argparse.ArgumentParser()
  parser.add_argument("-c", "--command", help = "command")
  parser.add_argument("-r", "--remote", help = "command")
  parser.add_argument("-l", "--local", help = "command")

  args = parser.parse_args()
  if args.command != None:
      args_command = args.command
  if args.remote != None:
      remote = args.remote
  if args.local != None:
      local = args.local

  if args_command != "":
     start(args_command)
  else:
    command = 'ffmpeg -i {} {}'.format(remote, local)
    start(command)

if __name__=="__main__":
  checkArgs()
  