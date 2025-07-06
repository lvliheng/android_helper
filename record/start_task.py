import time

from utils import Utils

def init(): 
  print("start_task")
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