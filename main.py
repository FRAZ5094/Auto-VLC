import vlc

media=vlc.MediaPlayer("Episode100.mkv")




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