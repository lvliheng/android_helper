import pyautogui

def getPixel(x, y):
  pixel = pyautogui.pixel(x, y)
  print("({}, {}) : {}".format(x, y, pixel))

def testPosition():
  try:
    while True:
        x, y = pyautogui.position()
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        print(positionStr, end='')
        print('\b' * len(positionStr), end='', flush=True)
  except KeyboardInterrupt:
      getPixel(x, y)

if __name__=="__main__":
  testPosition()