import music_tag
import yt_dlp
from moviepy.editor import AudioFileClip
import os
import random
import string
import glob
import json



def generate_code():
    return ''.join(random.choice(string.ascii_letters) for i in range(7))


def dl_audio(fname, url):
    
    stat = ""
    info_dict = ""
    input_file  = ""

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audiofiles/temp/rm.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            input_file = ydl.prepare_filename(info_dict)
            print("CHECK: ", input_file)
            audio_clip = AudioFileClip(input_file)
            audio_clip.write_audiofile(f"audiofiles/mp3s/{fname}.mp3")

    except yt_dlp.utils.DownloadError as e:
        return "S01"

    except OSError as e:
        print(e)
        return "S02"
    
    except Exception as e:
        return "S10"
    
    return "S00"
    



def tag(fname,title, artist, album, genre, year):

    dire = os.path.join("audiofiles/mp3s", f"{fname}.mp3")
    f = music_tag.load_file(str(r'{}'.format(dire)))
    
    tags = {
        "title": title,
        "artist": artist,
        "album": album,
        "genre": genre,
        "year": year
    }

    # TODO: test to see which below works

    for key, val in tags.items():
        if(val != ""):
            f[key] = val

    f.save()




def cleanup():

    try:
        
        if(os.path.exists("audiofiles/temp/rm.webm")):
            os.remove("audiofiles/temp/rm.webm")

        if(os.path.exists("audiofiles/temp/rm.m4a")):
            os.remove("audiofiles/temp/rm.m4a")

        files = glob.glob('audiofiles/mp3s/*')
        for f in files:
            os.remove(f)
        
        return
    
    except Exception as e:
        return "S03"

    

def get_quote():
    with open("quotes.json", "r") as file:
        quotes = json.load(file)
        # print(random.choice(quotes)["author"])
        # print(random.choice(quotes)["quote"])
        return random.choice(quotes)["quote"], random.choice(quotes)["author"]

# print(get_quote())


# cleanup()