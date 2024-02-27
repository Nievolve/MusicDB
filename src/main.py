import sqlite3
import os
import glob
import eyed3
import time
import constVaribel




#~12.9 milliseconds per track - Macbook Air 2017
print("Starting")
st = time.time()

def populateTable():
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

            # Use the GetBestDate method.
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
def polulateBackupTable():
    #Function variables
    count_track = 0
    count_album = 0
    list_album = []
    count_artist = 0
    list_artist = []

    # Database section
    conn = sqlite3.connect(constVaribel.database)
    c = conn.cursor()
    subfolder = []
    for folders in os.listdir(constVaribel.backupPath):
        subfolder.append(folders)

    for folder in range (0,len(subfolder)):
        mp3_path= glob.glob(os.path.join(constVaribel.backupPath+"/"+subfolder[folder], "*.mp3"))
        for mp3 in mp3_path:
            audiofile = eyed3.load(mp3)
            # Get tags in a varibel
            tag = audiofile.tag

            # Use the GetBestDate method.
            string_year = str(tag.getBestDate())


            # Check if the track already exists in the database
            c.execute("""SELECT * FROM backup_tracks WHERE title=? AND album=? AND artist=?""",
                    (audiofile.tag.title, audiofile.tag.album, audiofile.tag.artist))
            existing_track = c.fetchone()

            if not existing_track:
                c.execute("""INSERT INTO backup_tracks(title, album, artist, year) VALUES (?,?,?,?)""",
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
def createTable():
    conn = sqlite3.connect(constVaribel.database)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS tracks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            album TEXT,
            artist TEXT,
            year INTERGER) 
    """)
    c.execute("""CREATE TABLE IF NOT EXISTS backup_tracks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            album TEXT,
            artist TEXT,
            year INTERGER) 
    """)
    conn.commit()
    conn.close()
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
        print("Searching folders for new music")
        populateTable()
    elif menuChoice.lower() == "c" or menuChoice == "2":
        print("Creating table if not exist")
        createTable()
        print("Done")
        #Back up
    elif menuChoice.lower() == "r" or menuChoice == "3":
        polulateBackupTable()
    else:
        break

