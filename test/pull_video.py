import os

def pull_video():
  pc_path = "C:\\Users\\admin\\Downloads\\video\\"
  if not os.path.exists(pc_path):
    os.makedirs(pc_path)

  mobile_path = "/sdcard/Android/data/com.szbb.life/files/Media/video/"
  ls_command = "adb shell \"ls -R {}\"".format(mobile_path)

  file_names = os.popen(ls_command).readlines()
  for item in file_names:
    file_name = item.strip()
    ends_with_mp4 = file_name.endswith(".mp4")
    if ends_with_mp4:
      is_file_exists = os.path.exists("{}{}".format(pc_path, file_name))
      if not is_file_exists:
        pull_command = "adb pull {}{} {}".format(mobile_path, file_name, pc_path)
        os.system(pull_command)

if __name__=="__main__":
  pull_video()