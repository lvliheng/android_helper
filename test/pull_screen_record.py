import os
import datetime

def pull_screen_record():
  x = datetime.datetime.now()
  today = "{}{}{}".format(x.strftime("%Y"), x.strftime("%m"), x.strftime("%d"))
  ls_command = "adb -s W7X6R20429004861 shell \"ls -R /sdcard/Pictures/Screenshots/ | grep {}\"".format(today)

  file_names = os.popen(ls_command).readlines()
  for file_name in file_names:
    pull_command = "adb -s W7X6R20429004861 pull /sdcard/Pictures/Screenshots/{} C:\\Users\\admin\\Downloads\\".format(file_name.strip())
    os.system(pull_command)

if __name__=="__main__":
  pull_screen_record()