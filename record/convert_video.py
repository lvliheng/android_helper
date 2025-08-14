import os
from datetime import datetime, date, timedelta
from pathlib import Path
import time

def init():
  current = datetime.now()
  global year
  year = current.strftime("%Y")
  global month
  month = current.strftime("%m")

  global today
  today = date.today()

  global record_directory
  global stream_directory
  record_directory = "ScreenRecords"
  stream_directory = today
  Path(stream_directory).mkdir(parents = True, exist_ok = True)

  time.sleep(1)
  check_file_record()
  time.sleep(1)
  upload_file(today, year, month)

  time.sleep(1)
  yesterday = today - timedelta(days = 1)
  yesterday_year = yesterday.strftime("%Y")
  yesterday_month = yesterday.strftime("%m")
  upload_file(yesterday, yesterday_year, yesterday_month)
 
def check_file_record():
  global record_directory
  global stream_directory

  if Path(record_directory).is_dir():
    for file in os.listdir(record_directory):
      old_name = "{}\{}".format(record_directory, file)

      if not file.startswith("_") and file.endswith(".mp4") and os.path.getsize(old_name) > 20 * 1024 * 1024:
        global today
        current = datetime.now()
        today_millis = "{}-{}".format(today, current.strftime("%f"))
        new_name = "{}\_{}-screen.mp4".format(record_directory, today_millis)
        os.rename(old_name, new_name)

        output_file = "{}\{}-screen.mp4".format(stream_directory, today_millis)
        convert_file_format(new_name, output_file)

def convert_file_format(input_file, output_file):
  convert_command = "ffmpeg -i {} -c:v libx264 {}".format(input_file, output_file)
  os.system(convert_command)

def upload_file(today, year, month):
  upload_command = "bypy -v syncup D:\_temp\stream\{}\ /{}/{}/{}/".format(today, year, month, today)
  print('-----')
  print(upload_command)
  print('-----')
  os.system(upload_command)

if __name__=="__main__":
  try:
    init()
  except:
    None