import vlc
import glob
import json
import os
from tkinter import ttk
from tkinter import *
from pynput import keyboard
import time

json_file_name="settings.json"

global video,settings,current_episode,episodes,episode_i


def read_json():
    if os.path.exists(json_file_name):
        with open(json_file_name,"r") as f:
            subs=json.load(f)
        return subs
    else:
        return {}

def write_to_json(to_write):
    with open(json_file_name,"w") as f:
        json.dump(to_write,f,indent=4)

def colon_to_seconds(colon_time):
    colon=colon_time.find(":")
    mins=int(colon_time[:colon])
    secs=int(colon_time[colon+1:])
    time=int((mins*60)+secs)
    return time

def set_up_settings():
    ans=input("episode start (m:ss): ")
    time=colon_to_seconds(ans)
    settings["start"]=time*1000
    ans=input("time from end (m:ss): ")
    time=colon_to_seconds(ans)
    settings["from_end"]=time*1000
    settings["time"]=0
    return settings

settings=read_json()

def set_sub_dub():
    global video
    subs=video.video_get_spu_description()
    langs=video.audio_get_track_description()

    for sub in subs:
        if b"english" in sub[1].lower():
            video.video_set_spu(sub[0])

    for lang in langs:
        if b"japanese" in lang[1].lower():
            video.audio_set_track(lang[0])
            print(lang[0])

if settings=={}:
    print("no settings file")
    settings=set_up_settings()
else:
    print("settings file present")
    #print(settings)

episodes=glob.glob("*.mkv")
episodes=sorted(episodes,key=lambda x:[int(i) for i in x.split() if i.isdigit()])
#print(episodes)

if "episode" in settings.keys():
    current_episode=settings["episode"]
    episode_i=episodes.index(current_episode)
else:
    current_episode=episodes[0]
    episode_i=0

video=vlc.MediaPlayer(current_episode)


def while_video_playing_loop():
    global video,settings
    current_time=video.get_time()
    format_current_time=time.strftime("%M:%S",time.gmtime(int(current_time/1000)))
    max_length=video.get_length()
    max_time_format=time.strftime("%M:%S",time.gmtime(int(max_length/1000)))
    status_bar.config(text=f"{format_current_time}/{max_time_format}")
    episode_label.config(text=current_episode)
    if current_time<int(settings["start"]):
        video.set_time(int(settings["start"])+10)
        #print("skip")
    elif current_time>=max_length-int(settings["from_end"]) and max_length!=0:
        next()

    if max_length!=0:
        my_slider.config(value=int(current_time*100/max_length))

    status_bar.after(50,while_video_playing_loop)

root=Tk()
root.title("Video player")
root.geometry("300x300")

controls_frame=Frame(root)
controls_frame.pack()

def on_press(key):
    try:
        if key.char=="m":
            video.audio_toggle_mute()
    except: 
        if str(key)=="Key.right":
            forward()
        elif str(key)=="Key.left":
            backward()
        elif str(key)=="Key.space":
            video.pause()
        elif str(key)=="Key.esc":
            video.toggle_fullscreen()

def slide(pos):
    video.set_position(float(pos)/100)
    my_slider.config(value=pos)
    
    
def backward():
    current_time=video.get_time()
    current_time-=5000
    video.set_time(current_time)

def forward():
    current_time=video.get_time()
    current_time+=5000
    video.set_time(current_time)

def play():
    global video,settings
    video.play()
    time.sleep(1)
    video.set_time(int(settings["time"]))
    set_sub_dub()
    video.set_fullscreen(True)
    print(current_episode)
    while_video_playing_loop()

def next():
    global episode_i,video,current_episode
    episode_i+=1
    video.stop()
    current_episode=episodes[episode_i]
    print(current_episode)
    video=vlc.MediaPlayer(episodes[episode_i])
    video.play()
    time.sleep(1)
    set_sub_dub()
    video.set_fullscreen(True)


pause_btn=Button(controls_frame,text="Pause",command=video.pause)
next_btn=Button(controls_frame,text="Next",command=next)
episode_name=Label(root)

pause_btn.grid(row=0,column=1)
next_btn.grid(row=0,column=2)

def on_closing():
    settings["episode"]=current_episode
    settings["time"]=video.get_time()
    write_to_json(settings)
    video.stop()
    root.destroy()

status_bar=Label(root,text="",bd=1,relief=GROOVE,anchor="e")
status_bar.pack(fill=X,side=BOTTOM,ipady=2)

my_slider=ttk.Scale(root,from_=0,to=100,orient=HORIZONTAL,value=0,command=slide,length=150)
my_slider.pack(pady=20)
episode_label=Label(root,text="")
episode_label.pack(pady=10)
listener = keyboard.Listener(on_press=on_press)
listener.start()


play()
video.audio_set_mute(False)




root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
