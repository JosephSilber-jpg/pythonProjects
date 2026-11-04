# Before running:
# make sure you have spotdl installed 
# (pip install spotdl, spotdl --download-ffmpeg)
#
# to download a spotify playlist, run the following command in your terminal:
# spotdl download { playlist link }
#
# when you copy the link, make sure to delete 
# everything after the first question mark, and the question mark itself
# otherwise spotdl will throw an error

from pathlib import Path
import os
import eyed3

allFiles = Path("")
destination = Path('spotdl_output')

newAlbumName = "MONEY MIXTAPE NO. 2"

i = 1
for file in allFiles.iterdir():
    if file.name.endswith('.mp3'):
        # Process the mp3 file
        mp3 = eyed3.load(file)
        mp3.tag.album = newAlbumName
        # mp3.tag.track_num = i
        mp3.tag.save()

        file.rename(destination / file.name)
        i += 1
    else:
        # Handle other file types or ignore
        continue