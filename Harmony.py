import threading
import os
import time
import tkinter.messagebox
from mutagen import mp3
import pygame
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from pygame import mixer
from ttkthemes import themed_tk as tk1
from mutagen.mp3 import MP3
from datetime import datetime
import tkinter as tk
from ttkthemes import *
from PIL import Image


def func():
    #Window Details
    window = tk1.ThemedTk()
    window.title("Audio Player")
    window.geometry('300x460')
    window.get_themes()
    window.set_theme("black")


    music_player_controls = ttk.Label(window, text = "v1.0", anchor = S)

#mixer initialier
    pygame.mixer.init()

    music_progress = tk.StringVar()
    song_length_label = tk.StringVar()


#1st Frame
    frame = Frame(window)
    frame.pack()


#About the application
    def about():
        tkinter.messagebox.showinfo('About',"Designed by Raju Das\nAudio Player using Python and Tkinter Module. v1.0")

    def choose_theme():
        theme_window = Tk()
        theme_window.title("Themes")
        theme_window.geometry('300x350')


#Extracting tracks from the folder directory
    folder = '/home/firehawk-69/Desktop/Music'
    filelist = [fname for fname in os.listdir(folder) if fname.endswith('.wav')]
    song_menu = ttk.Combobox(window, values=filelist, state='normal')
    song_menu.pack(fill='x')

    
    canvas_for_image = Canvas(window, bg='black', height=170, width = 290)
    canvas_for_image.pack()
    

    def show_details(play_song):
    
        a = mixer.Sound(play_song)
        total_length = a.get_length()

        (mins,secs) = divmod(total_length, 60)
        mins = round(mins)
        secs = round(secs)

        t2 = threading.Thread(target=start_count, args=(total_length,))
        t2.start()
        


    def start_count(t):

        current_time = 0
        while(current_time<=t):
        
            mins,secs = divmod(current_time,60)
            mins = round(mins)
            secs = round(secs)

            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            length = f'{round(t)//60}:{round(t)%60}'
            music_progress.set(timeformat)          
            song_length_label.set(length)
            #song_progress['value']+= 0.40
            time.sleep(1)
            current_time+=1    


    def play_song():                    

        song = song_menu.get()              #name of the song
        music_player_controls['text'] = f'{song}'
        song = f'/home/firehawk-69/Desktop/Music/{song}'
        pygame.mixer.music.load(song)
        show_details(song)
        pygame.mixer.music.play()
    

    progress_frame = Frame(window)
    progress_frame.pack()

    #song_progress = ttk.Progressbar(progress_frame, orient=HORIZONTAL, length=290, mode='determinate')  #bar
    #song_progress.pack(pady=3)

    current_label = ttk.Label(progress_frame, textvariable = music_progress)                #song status
    current_label.pack(side='left')

    length_label = ttk.Label(progress_frame , textvariable = song_length_label)
    length_label.pack(side='right')


    buttonFrame = Frame(window)
    buttonFrame.pack()


    def stop_song():
    
        pygame.mixer.music.stop()
        music_player_controls['text'] = "Stopped"
        #song_progress.stop()
    

    def volume_set(x):
    
        volume = float(x)/100
        mixer.music.set_volume(volume)
    #music_player_controls["text"] = "{}".format(round(volume*100))
    

    def forward_song():
 
        next_track_index = song_menu.current()+1
        song = filelist[next_track_index]
        song = f'/home/firehawk-69/Desktop/Music/{song}'
        song_menu.set(filelist[next_track_index])
        pygame.mixer.music.load(song)
        show_details(song)
        pygame.mixer.music.play()

        song = song.replace('/home/firehawk-69/Desktop/Music/',"")
        music_player_controls['text'] = f'{song}'

    global count
    count = 0

    def rewind_track():
        global count
        count+=1
        if(count<2): play_song()
        else:
            prev_track_index = song_menu.current()-1
            song = filelist[prev_track_index]
            #function call for showing time details
            song = f'/home/firehawk-69/Desktop/Music/{song}'
            song_menu.set(filelist[prev_track_index])
            pygame.mixer.music.load(song)
            pygame.mixer.music.play()
            #song_progress.start(10)

            song = song.replace('/home/firehawk-69/Desktop/Music/',"")
            music_player_controls['text'] = f'{song}'

            count=0
            
#Frames
    bottomFrame = Frame(window)
    bottomFrame.pack(side = BOTTOM)

# Text Buttons
    add_button = Button(bottomFrame, text = '+Add')
    del_button = Button(bottomFrame, text = '-Del')
    about_button = Button(bottomFrame, text = 'About', command=about)
    theme_button = Button(bottomFrame, text = "Themes", command=choose_theme)

#graphical Button
    play_Button_image = PhotoImage(file = '/home/firehawk-69/Desktop/PlayerImages/play.png')
    play_button = Button(buttonFrame, image=play_Button_image, relief='flat', command = play_song)

    forward_button_image = PhotoImage(file = '/home/firehawk-69/Desktop/PlayerImages/forward.png')
    forward_button = Button(buttonFrame, image=forward_button_image, relief='flat', command = forward_song)

    rewind_button_image = PhotoImage(file = '/home/firehawk-69/Desktop/PlayerImages/backward.png')
    rewind_button = Button(buttonFrame, image=rewind_button_image, relief='flat', command = rewind_track)

    stop_button_image = PhotoImage(file = '/home/firehawk-69/Desktop/PlayerImages/stop.png')
    stop_button = Button(buttonFrame, image=stop_button_image, relief='flat', command = stop_song)


#Alphabetical Buttons
    add_button.pack(side=LEFT)
    del_button.pack(side=LEFT)
    about_button.pack(side=LEFT)
    theme_button.pack(side=LEFT)

    #Graphical Buttons
    rewind_button.grid(row=0, column=0)
    play_button.grid(row=0,column=1)
    forward_button.grid(row=0,column=3)
    stop_button.grid(row=0,column=4)


    volume_frame = Frame(window)
    volume_frame.pack()

    volume_slider = ttk.Scale(volume_frame, from_= 0, to = 100, orient = HORIZONTAL, command=volume_set)
    volume_slider.set(40)
    mixer.music.set_volume(0.4) 

    volume_slider.grid(pady=10)
    music_player_controls.pack(pady=31,fill=X)

    def on_closing():
        stop_song()
        window.destroy()

    window.protocol("", on_closing)
    window.mainloop()

t1 = threading.Thread(target=func)
t1.start()
t1.join()    
