import json
import subprocess
from random import randint
import psutil

playing = False
lastSong = 0
song = 0

while True:
    try:
        with open('configs/songs.json') as data:
            rdio = json.load(data)
        while song == lastSong:
            song = randint(1, len(rdio))
        lastSong = song
        rdio[str(song)]['nowplaying'] = 'true'
        with open('configs/songs.json', 'w') as data:
            json.dump(rdio, data, indent=4)
        print("\nNow playing " + rdio[str(song)]['name'] + " by " + rdio[str(song)]['artist'] + ".")
        subprocess.check_call("./sam Now playing " + rdio[str(song)]['name'] + " by " + rdio[str(song)]['artist'] + ".", shell=True)
        playing = True
        subprocess.check_call('cvlc --play-and-exit "' + rdio[str(song)]['location'] + '"', shell=True)
        playing = False
        with open('configs/songs.json') as data:
            rdio = json.load(data)
        rdio[str(song)]['nowplaying'] = 'false'
        with open('configs/songs.json', 'w') as data:
            json.dump(rdio, data, indent=4)
    except (KeyboardInterrupt, subprocess.CalledProcessError):
        if not playing:
            raise
        else:
            for proc in psutil.process_iter():
                if proc.name() == 'vlc':
                    proc.kill()
            playing = False
            with open('configs/songs.json') as data:
                rdio = json.load(data)
            rdio[str(song)]['nowplaying'] = 'false'
            with open('configs/songs.json', 'w') as data:
                json.dump(rdio, data, indent=4)
            subprocess.call("./sam Song was skipped.", shell=True)
