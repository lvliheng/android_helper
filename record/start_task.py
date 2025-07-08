from datetime import datetime
import time

from utils import Utils

def init(): 
  start_hour = 19
  start_minute = 50
  stream_refresh_hour = 1
  current_time = datetime.now()
  start_date_time = datetime(current_time.year, current_time.month, current_time.day, start_hour, start_minute)
  global end_date_time
  end_date_time = datetime(current_time.year, current_time.month, current_time.day, start_hour + stream_refresh_hour, start_minute)

  need_check_time = False
  if need_check_time:
    if current_time > start_date_time and current_time < end_date_time:
      start()
  else:
    start()
    
def start():
  time.sleep(1)
  Utils.hot_key_safely(["win", "right"])
  time.sleep(1)
  Utils.hot_key_safely(["win", "up"])
  time.sleep(1)
  Utils.hot_key_safely(["ctrl", "shift", "t"])
  time.sleep(1)
  Utils.write_safely("cd D:\_temp\stream", "enter")
  time.sleep(1)
  Utils.hot_key_safely(["ctrl", "shift", "t"])
  time.sleep(1)
  Utils.write_safely("cd D:\_temp\stream", "enter")
  time.sleep(1)
  Utils.write_safely("record_stream", "enter")

if __name__=="__main__":
  try:
    init()
  except Exception as e:
    Utils.print_with_datetime("-cancel\n{}".format(e))
  except KeyboardInterrupt:
    None