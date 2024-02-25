import sqlite3
import os
import glob
import eyed3
import logging
import time
import constVaribel
import create_db_and_table
#~12.9 milliseconds per track - Macbook Air 2017
print("Starting")
st = time.time()
# Logging section
LOG_FORMAT = ("%(asctime)s, %(lineno)d, %(levelname)s, %(message)s")
logging.basicConfig(filename="resources/test_main.log",
                    level=logging.INFO,
                    filemode="w",
                    format=LOG_FORMAT)
logger = logging.getLogger()
def populate():
    #Function variables
    count_track = 0
    count_album = 0
    list_album = []
    count_artist = 0
    list_artist = []

    # Database section
    conn = sqlite3.connect(constVaribel.database)
    c = conn.cursor()

    # Subfolder is a list of subfolders in musik
    subfolder = []
    # Forloop which polulate subfolder list with name of subfolders.
    for k in os.listdir(constVaribel.local_path): 
        subfolder.append(k)
    #Goes into each subfolder and looks for mp3 files to extract metadata and insert.
    for folder in range (0,len(subfolder)):
        mp3_path= glob.glob(os.path.join(constVaribel.local_path+"/"+subfolder[folder], "*.mp3"))
        for mp3 in mp3_path:
            audiofile = eyed3.load(mp3)
            # Get tags in a varibel
            tag = audiofile.tag

            # Use the GetBestDate method. ISSUE TO BE FIXED
            string_year = str(tag.getBestDate())


            # Check if the track already exists in the database
            c.execute("""SELECT * FROM tracks WHERE title=? AND album=? AND artist=?""",
                    (audiofile.tag.title, audiofile.tag.album, audiofile.tag.artist))
            existing_track = c.fetchone()

            if not existing_track:
                c.execute("""INSERT INTO tracks(title, album, artist, year) VALUES (?,?,?,?)""",
                        (audiofile.tag.title, audiofile.tag.album, audiofile.tag.artist, string_year))
                print("Added:")
                print("Track: " + audiofile.tag.title)
                count_track += 1
                print("Album: " + audiofile.tag.album)
                if audiofile.tag.album not in list_album:
                    list_album.append(audiofile.tag.album)
                    count_album += 1
                else:
                    pass
                print("Artist: " + audiofile.tag.artist)

                if audiofile.tag.artist not in list_artist:
                    list_artist.append(audiofile.tag.artist)
                    count_artist += 1
                else:
                    pass

                print("Year: " + string_year)
                conn.commit()
            else:
                
                print("Track already exists: " + audiofile.tag.title)

    conn.close()
    print("You added:")
    print(count_track, " tracks")
    print(count_album, " albums")
    print(count_artist, " artists")
#Main menu
while True:
    print("     Main Menu")
    print("1: [P]opulate")
    print("2: [C]reate Table")
    print("3: [R]emove Data")
    print("4: Read [D]ata")
    print("5: [Q]uit")
    menuChoice = input(" Your choice:")
    if menuChoice == "p" or menuChoice == "1":
        populate()
    elif menuChoice.lower() == "c" or menuChoice == "2":
        create_db_and_table.create_database_and_table()
    else:
        break

