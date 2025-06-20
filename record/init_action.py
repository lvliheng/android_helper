import pyautogui
from pynput import keyboard
from pathlib import Path

def init():
  global action_list
  action_list = ["setting_button", "selecte_item", "search_input_box", "refresh_button", 
    "load_all", "window_top", "host_title", "value_input_box"]
  global current_index
  current_index = 0
  global result
  result = "#{}".format(action_list[current_index])
  
  global action_config_file
  action_config_file = "action_config"
  if not Path(action_config_file).exists():
    open(action_config_file, "w")
  
  print("#{}".format(action_list[current_index]))
  
  start_keyboard_listener()

def start_keyboard_listener():
  global listener
  listener = keyboard.Listener(on_press=on_press)
  listener.start()
  listener.join()
  
def on_press(key):
  global listener
  if key == keyboard.Key.esc:
    listener.stop()
    print("cancel")
  elif key == keyboard.Key.enter:
    global result
    position = get_position()
    print(position)
    result += "\n{}".format(position)
    global current_index
    current_index += 1
    
    global action_list
    if current_index >= len(action_list):
      print("done")
      set_config(result)
      
      listener.stop()
      return
    result += "\n#{}".format(action_list[current_index])
    print("#{}".format(action_list[current_index]))

def get_position():
  x, y = pyautogui.position()
  return "{},{}".format(x, y)

def set_config(content):
  global action_config_file
  file = open(action_config_file, "w")
  file.write(content)
  file.close()

if __name__=="__main__":
  try:
    init()
  except Exception as e:
    print(e)
  except KeyboardInterrupt:
    None