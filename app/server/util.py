import music_tag
import yt_dlp
from moviepy.editor import AudioFileClip
import os
import random
import string
import glob


def generate_code():
    return ''.join(random.choice(string.ascii_letters) for i in range(7))


def dl_audio(fname, url):

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audiofiles/temp/rm.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        input_file = ydl.prepare_filename(info_dict)
        print("CHECK: ", input_file)


    audio_clip = AudioFileClip(input_file)
    audio_clip.write_audiofile(f"audiofiles/mp3s/{fname}.mp3")
    # os.remove("audiofiles/temp/rm.webm")
    # TODO: maybe remove later (below)
    if(os.path.isdir("audiofiles/temp/rm.webm")):
        os.remove("audiofiles/temp/rm.webm")
        print("webm")
    elif (os.path.isdir("audiofiles/temp/rm.m4a")):
        os.remove("audiofiles/temp/rm.m4a")
        print("m4a")




def tag(fname,title, artist, album, genre):

    dire = os.path.join("audiofiles/mp3s", f"{fname}.mp3")
    f = music_tag.load_file(str(r'{}'.format(dire)))
    
    tags = {
        "title": title,
        "artist": artist,
        "album": album,
        "genre": genre
    }

    # TODO: test to see which below works

    for key, val in tags.items():
        if(val != ""):
            f[key] = val

    f['title'] = title
    f['artist'] = artist
    f['album'] = album
    f['genre'] = genre

    f.save()




def cleanup():
    
    if(os.path.exists("audiofiles/temp/rm.webm")):
        os.remove("audiofiles/temp/rm.webm")

    if(os.path.exists("audiofiles/temp/rm.m4a")):
        os.remove("audiofiles/temp/rm.m4a")

    files = glob.glob('audiofiles/mp3s/*')
    for f in files:
        os.remove(f)
    

# cleanup()


