from pynput import keyboard
from time import sleep
def on_press(key):
    print(f"pressed: {key}")

def on_release(key):
    pass

def check_time():
    print("checking time")
    sleep(1)
    check_time()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(on_press=on_press)

listener.start()
check_time()
