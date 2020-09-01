from tkinter import *
import time
import vlc
from tkinter import ttk
from pynput import keyboard

def while_video_playing_loop():
    current_time=video.get_time()
    format_current_time=time.strftime("%M:%S",time.gmtime(int(current_time/1000)))
    max_length=video.get_length()
    max_time_format=time.strftime("%M:%S",time.gmtime(int(max_length/1000)))
    status_bar.config(text=f"{format_current_time}/{max_time_format}")
    start_time=90000
    end_time=140000
    if current_time<start_time:
        video.set_time(start_time+10)
    elif current_time>=max_length-end_time:
        video.stop()

    if max_length!=0:
        my_slider.config(value=int(current_time*100/max_length))

    status_bar.after(50,while_video_playing_loop)

global video
video=vlc.MediaPlayer("Original/[AnimeRG] Naruto - 001 Enter Naruto Uzumaki! [720p] [x265] [pseudo].mkv")
root=Tk()
root.title("Video player")
root.geometry("200x100")

controls_frame=Frame(root)
controls_frame.pack()

def on_press(key):
    print(key)
    if str(key)=="Key.right":
        forward()
    if str(key)=="Key.left":
        backward()


def slide(pos):
    #print(pos)
    video.set_position(float(pos)/100)
    
def backward():
    current_time=video.get_time()
    current_time-=5000
    video.set_time(current_time)

def forward():
    current_time=video.get_time()
    current_time+=5000
    video.set_time(current_time)

def play():
    video.play()
    while_video_playing_loop()

play_btn=Button(controls_frame,text="Play",command=play)
pause_btn=Button(controls_frame,text="Pause",command=video.pause)
exit_btn=Button(controls_frame,text="Forward",command=forward)


play_btn.grid(row=0,column=0)
pause_btn.grid(row=0,column=1)
exit_btn.grid(row=0,column=2)

def on_closing():
    video.stop()
    root.destroy()

status_bar=Label(root,text="",bd=1,relief=GROOVE,anchor="e")
status_bar.pack(fill=X,side=BOTTOM,ipady=2)

my_slider=ttk.Scale(root,from_=0,to=100,orient=HORIZONTAL,value=0,command=slide,length=150)
my_slider.pack(pady=20)

listener = keyboard.Listener(on_press=on_press)
listener.start()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
