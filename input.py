from pynput import keyboard
from time import sleep
import sys
def on_press(key):
    print(key)
    try:
        if key.char=="e":
            print("pressed e")
        if key.char=="q":
            listener.stop()
            print("exited")
            sys.exit(0)
        if str(key)=="<104>":
            print("pressed up arrow") 
    except:
        print("key.char doesnt work")
        print(key)

listener = keyboard.Listener(on_press=on_press)

listener.start()

try:
    while True:
        sleep(100)
except:
    listener.stop()