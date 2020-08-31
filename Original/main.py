import vlc
import glob
import json
import os

json_file_name="settings.json"

def on_quit(current_episode,settings):
    settings["episode"]=current_episode
    write_to_json(settings)

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
    return settings

settings=read_json()

if settings=={}:
    print("no settings file")
    settings=set_up_settings()
else:
    print("settings file")
    print(settings)


files=glob.glob("Original/*.mkv")

if "episode" in settings.keys():
    current_episode=settings["episode"]
else:
    current_episode=files[0]

#on_quit(current_episode,settings)



#media=vlc.MediaPlayer("Episode100.mkv")

"""
media.get_time()
media.set_time()#im ms
media.set_position from 0 to 1.0
media.video_set_spu()

media.audio_get_track_description() #get available audio tracks
media.video_get_track_description()

media.audo_toggle_mute()
media.audio_set_track()
media.video_set_crop_geometry(psz_geometry)

end 2:20 from end
"""