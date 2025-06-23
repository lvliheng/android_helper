import pyautogui
import argparse

def getPixel(x, y):
  pixel = pyautogui.pixel(x, y)
  print("({}, {}) : {}".format(x, y, pixel))

def getPosition():
  try:
    while True:
        x, y = pyautogui.position()
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        print(positionStr, end='')
        print('\b' * len(positionStr), end='', flush=True)
  except KeyboardInterrupt:
      getPixel(x, y)

def string_to_int(value):
  try:
    result = int(value)
    return result
  except:
    return -1

def init():
  input_x = -1
  input_y = -1
    
  parser = argparse.ArgumentParser()
  parser.add_argument("-x", "--x", help = "point x")
  parser.add_argument("-y", "--y", help = "point y")

  args = parser.parse_args()
  if args.x != None:
    input_x = string_to_int(args.x)
  if args.y != None:
    input_y = string_to_int(args.y)
  
  if input_x == -1 or input_y == -1:
    getPosition()
  else:
    getPixel(input_x, input_y)
    
if __name__=="__main__":
  init()