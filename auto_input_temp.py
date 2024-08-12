import pyautogui
import time
import clipboard
import random
from datetime import datetime

def init():
    start() 

def start():
    last = 0
    start = round(time.time())

    while True:
        #refresh
        duration = random.randint(5, 8)
        # duration = random.randint(5, 10)
        time.sleep(duration)
        # pyautogui.click(1130, 200)
        # pyautogui.click(1130, 200)
        pyautogui.click(1200, 300)
        pyautogui.hotkey("ctrl", "r")
        time.sleep(2)

        #focus
        pyautogui.click(1200, 300)
        time.sleep(.2)
        pyautogui.hotkey("command", "a")
        time.sleep(.2)
        pyautogui.hotkey("command", "c")

        try:
            current = int(clipboard.paste())
        except:
            break

        if current <= 0 or current > 160000:
            break
        elif current - last > 3000:
            last = current
            time.sleep(.2)
        else :
            add = random.randint(800, 1200)
            # add = random.randint(500, 1000)
            current += add
            pyautogui.click(1200, 300)
            pyautogui.hotkey("command", "a")
            time.sleep(.2)
            pyautogui.write(str(current))

            time.sleep(.2)
            pyautogui.hotkey("command", "s")
            now = round(time.time())
            print("{}(+{}): {}(+{})".format(datetime.now(), now - start, current, add))
            start = now
            last = current

if __name__=="__main__":
    init()