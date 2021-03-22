import csv
from pytube import YouTube
from moviepy.editor import *
import os
import random
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error,TIT2, TPE1, TPE2
import time



#Menu 
def menu():
    print('\n')
    print('=====================================')
    print('|                                   |')
    print('| WELCOME TO IIIGIV SONG DOWNLOADER |')
    print('|                                   |')
    print('|  CREATED BY : VIGNESH VENKATESH   |')
    print('|                                   |')
    print('=====================================')
    print('\n')
    print("=============================")
    print("| ENTER 1 TO BEGIN DOWNLOAD |")
    print("| ENTER 2 TO EXIT           |")
    print("=============================")
    print('\n')
    choice = int(input("Enter Choice:"))
    if choice == 1:
        start()
    elif choice == 2:
        exit()
    else:
        print('\n')
        print("=================")
        print("| INVALID INPUT |")
        print("=================")
        menu()

#This is where everything begins
def start():
    #Checks for directories in the folder
    directories = os.listdir()
    #Checks if 'Video' directory exists in the folder
    if 'Video' not in directories:
        print('\n')
        print("=============================")
        print("|          ERROR            |")
        print("=============================")
        print("|  Video Folder is missing  |")
        print("|============================")
        print("|Please create the folder   |")
        print("|and restart the program    |")
        print("=============================")
        time.sleep(5)
    #Checks if 'Audio' directory exists in the folder
    if 'Audio' not in directories:
        print('\n')
        print("=============================")
        print("|          ERROR            |")
        print("=============================")
        print("|  Audio Folder is missing  |")
        print("|============================")
        print("|Please create the folder   |")
        print("|and restart the program    |")
        print("=============================")
        time.sleep(5)
        
    print('\n')
    file_name = input('Enter (text) file name where you have stored the data:')
    if file_name[-4:]!='.txt':
        print('\n')
        print('==========================')
        print('| INVALID FILE EXTENSION |')
        print('==========================')
        menu()


    print('\n')
    #Asking user input, if the user wants to add their own album art in random order
    choice = input("Do you wish to add your custom album art in random order? [Y/N]: ")
    choice = choice.upper()
    
    if choice == 'Y':
        
        album_art = True
        print('\n')
        #Checks if 'Album_Art' directory exists in the folder, only if the user enters Y for the prev choice
        if 'Album_Art' not in directories:
            print("=============================")
            print("|          ERROR            |")
            print("=============================")
            print("|Album_Art Folder is missing|")
            print("|============================")
            print("|Please create the folder   |")
            print("|and restart the program    |")
            print("=============================")
            time.sleep(5)
        #Lists files in the 'Album_Art' directory
        files = os.listdir('Album_Art/')
        #Prints an error message if there are no files present
        print('\n')
        ctr = 0
        for i in files:
            if i[-4:]=='.png' or i[-4:]=='.jpg' or i[-5]=='.jpeg':
                ctr=ctr+1
        #Checks if any pictures exist in the directory
        if ctr==0:
            print("===================================")
            print("|NO PICTURES PRESENT IN THE FOLDER|")
            print("===================================")
            menu()
            
    elif choice == 'N':
        album_art = False
        
    else:
        print('\n')
        print('=================')
        print('| INVALID INPUT |')
        print('|================')

    downloader(file_name,album_art)


def downloader(file_name,album_art):

    original_list = []
    new_list = []

    #opening csv/txt file to read
    with open(file_name,'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        for i in csv_reader:
            original_list.append(i)

        original_list = original_list[1:]

    if len(original_list) == 0:
        print('\n')
        print("========================")
        print("| NO SONGS TO DOWNLOAD |")
        print("========================")
        menu()


    first_row = ['SONG NAME', 'ARTIST','SONG LINK']
    new_list.append(first_row)
    new_list = new_list+original_list

    
    for i in original_list:
        if len(i) == 0:
            continue
        
        elif len(i) >0:
            #Downloading songs from youtube
            myVideo = YouTube(i[2])
            print('\n')
            print('='*70)
            video_title = myVideo.title
            print('Video Title:',video_title)
            myVideo.streams.first().download('Video/')

            #Converting mp4 to mp3
            path = 'Video/'
            files = os.listdir(path)
            for j in files:
                mp4_file = 'Video/'+j
                mp3_file = 'Audio/'+j[:-4]+'.mp3'
            videoClip = VideoFileClip(mp4_file)
            audioClip = videoClip.audio
            audioClip.write_audiofile(mp3_file)
            audioClip.close()
            videoClip.close()
            os.remove(mp4_file)


            mp3_path = mp3_file

            #Editing the mp3 metadat ID3 tags
            title = i[0]
            artist = i[1]
            
            print('Title:',title)
            print('Artist:',artist)
            
            tag = ID3()
            tag.add(TIT2(encoding=3, text=(title))) #Editing Title ID3 tag
            tag.add(TPE1(encoding=3, text=(artist))) #Editing Artist ID3 tag
            tag.add(TPE2(encoding=3, text=(artist))) #Editing Song Artist ID3 tag
            tag.save(mp3_path, v2_version=3)

            #Adding album art
            if album_art == True:
                path = 'Album_Art/'
                audio = MP3(mp3_path, ID3=ID3)
                try:
                    audio.add_tags()
                except error:
                    pass

                files = os.listdir('Album_Art/')
                arts = []
                for j in files:
                    if j[-4:]=='.png' or j[-4:]=='.jpg' or j[-5:]=='.jpeg':
                        arts.append(j)
                    
                art = random.choice(arts)
                print('ART CHOSEN:',art[:-4])
                art_path = 'Album_Art/'+art
                audio.tags.add(APIC(mime='image/jpeg',type=3,desc=u'Cover',data=open(art_path,'rb').read()))
                audio.save()

            
            print("DOWNLOAD COMPLETED")
            print("="*70)

            #Edits text file to remove converted/download
            new_list.remove(i)

            f = open(file_name,'w')
            for i in new_list:
                str = f'{i[0]},{i[1]},{i[2]}\n'
                f.write(str)
            f.close()
        

    menu()
    

    
menu()


    
