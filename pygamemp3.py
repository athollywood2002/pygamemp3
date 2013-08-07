import sys
import Tkinter
import tkMessageBox
import tkFileDialog
import ttk
from mp3_modules import *
from Tkinter import *
from mutagen.easyid3 import EasyID3
from glob import glob
from mutagen.mp3 import MP3
import pygame
import datetime



myGui = Tk()
           
myGui.title("Your Mp3")
myGui.geometry("405x160+400+150")

''' Global variables '''
paused = False
myopen = None
var = None
artist_var = None
album_var = None
title_var = None
album_info = Tkinter.StringVar()
artist_info = Tkinter.StringVar()
title_info = Tkinter.StringVar()
audio = MP3(myopen)
track_len = Tkinter.StringVar()
value_progress = Tkinter.StringVar()



''' modules '''
#opens the file chooser menu

def mOpen():
    global myopen
    global audio
    myopen = tkFileDialog.askopenfilename(
                       filetypes=[('MP3','*.mp3')],
                       initialdir="/home/david/Music/"
        )
    
    
        


def mClose():
    mExit = tkMessageBox.askokcancel(title="Quit", message="are you sure?")
    if mExit ==True:
        myGui.destroy()
        return
    
def mPlay():
    global myopen
    global var
    pygame.mixer.init()
    pygame.mixer.music.load(myopen)
    pygame.mixer.music.play()
    album_info.set(album())
    artist_info.set(artist())
    title_info.set(title())
    track_len.set(track_length())
    position()
    

def play_pause():
    global paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True
        

def mStop():
    pygame.mixer.music.stop()

    
def mVolume(x):
    pygame.mixer.init()
    x = vol.get()/10.0
    pygame.mixer.music.set_volume(x)


''' gets track info and song info from within mp3 '''

''' track length  '''

def track_length():
    global myopen
    audio = MP3(myopen)
    mill_length = (audio.info.length*1000)
    progressbar["maximum"] = mill_length
    return ("%.2f" % (audio.info.length/60))

def track_len_sec():
    global myopen
    global audio_len_time
    audio_len = MP3(myopen)
    return (audio_len.info.length*1000)
   
''' gets play position of current track '''

def position():
    global value_progress
    if pygame.mixer.music.get_busy() == True: 
        value_progress.set(float(pygame.mixer.music.get_pos()))
        button_frame.after(50, position)


#new track infomation modules

def album():
    global myopen
    global var
    global album_var
    for filename in glob(myopen):
        mp3info = EasyID3(filename)
        var = mp3info.items()
        for i in var:
            if "album" in i[0]:
                album_var = str(i[1])
                return album_var.strip('[\'\",u]')
            else:
                None


def artist():
    global myopen
    global var
    global artist_var
    for filename in glob(myopen):
        mp3info = EasyID3(filename)
        var = mp3info.items()
        for i in var:
            if "artist" in i[0]:
                artist_var = str(i[1])
                return artist_var.strip('[\'",u]')
            else:
                None

def title():
    global myopen
    global var
    for filename in glob(myopen):
        mp3info = EasyID3(filename)
        var = mp3info.items()
        for i in var:
            if "title" in i[0]:
                title_var = str(i[1])
                return title_var.strip('[\'\",u]')
            else:
                None




''' Menu Construction '''

menubar=Menu(myGui)


''' File Menu '''
filemenu =Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command= mOpen)
filemenu.add_command(label="Close", command = mClose)

menubar.add_cascade(label="File", menu=filemenu)


myGui.config(menu=menubar)


''' Frame to wrap INFO and Progress Bar '''
main_frame = LabelFrame(myGui, border=5,)
main_frame.pack(pady=0)


'''Frame for all information  '''
info_frame = LabelFrame(main_frame, border = 2, relief=SUNKEN,
                        background='white', width =400,
                        height=80)
info_frame.pack(ipady=0)
info_frame.pack_propagate(0)


''' Frame for Title, Artist ..... ''' 
station_grid = LabelFrame(info_frame,border=0,
                          background='white', width=100,
                          height=80)
station_grid.pack(side=LEFT, expand=FALSE)
station_grid.propagate(0)

#Label for Artist
artist_label = Label(station_grid, anchor=E, 
                     background='white', text= "Artist :")
artist_label.pack(fill=X)

#Label for Song
song_title = Label(station_grid, anchor=E,
                   background='white', text= "Song :")
song_title.pack(fill=X)

#Label for Album
album_title = Label(station_grid, anchor=E,
                    background='white', text= "Album :")
album_title.pack(fill=X)

#Label for Song Length
length_title = Label(station_grid, anchor=E,
                     background='white', text= "Length :", )
length_title.pack(fill=X)


''' Frame for Information from Tag Functions ..... '''

function_grid = LabelFrame(info_frame, border=0,
                           background='white', width=300,
                           height=80)
function_grid.pack(side=LEFT, padx=20)
function_grid.propagate(0)


#Artist Info from Tags
artist_info_label = Label(function_grid, anchor=W,
                          background='white',
                          textvariable=artist_info)
artist_info_label.pack(fill=X)


#Title info from Tags
title_info_label = Label(function_grid, anchor=W,
                         background='white',
                         textvariable=title_info)
title_info_label.pack(fill=X)

#Album Info from Tags
album_info_label = Label(function_grid, anchor=W,
                         background='white', textvariable=album_info)
album_info_label.pack(fill=X)


#Length Info for from Tags
length = Label(function_grid, anchor=W,
               background="white", textvariable=track_len)
length.pack(fill=X)



''' song progress bar '''
# Progressbar Frame
y= LabelFrame(main_frame, width=400,border = 0, height=10, relief=RAISED)
y.pack(pady=0, padx=0)
y.pack_propagate(0)


progressbar = ttk.Progressbar(y, orient=HORIZONTAL,
                              length=400, mode="determinate",
                              variable=value_progress
                              )
progressbar.pack(side=BOTTOM, pady=0, padx=0)


''' Frame for controls '''

control_frame = LabelFrame(main_frame, border = 0, width =400)
control_frame.pack(pady=0, padx=0, ipadx=0, ipady=0)

'''Frame for buttons'''

button_frame = LabelFrame(control_frame, relief=RAISED,)
button_frame.pack(side=LEFT)

''' Stop Button '''
mButton_stop = Button(button_frame, command = mStop)
photo_stop=PhotoImage(file="/home/david/Pictures/software_icons/stop.gif")
mButton_stop.config(image=photo_stop)
mButton_stop.pack(side=LEFT)

'''Play Button'''
mButton_play = Button(button_frame, command = mPlay)
photo_play=PhotoImage(file="/home/david/Pictures/software_icons/play.gif")
mButton_play.config(image=photo_play,)
mButton_play.pack(side=LEFT)


'''Pause Button '''
mButton_pause = Button(button_frame, command = play_pause)
photo_pause=PhotoImage(file="/home/david/Pictures/software_icons/pause.gif")
mButton_pause.config(image=photo_pause)
mButton_pause.pack(side=LEFT)



''' Power Button, Closes App'''
mButton_close = Button(button_frame, command = mClose)
photo_power=PhotoImage(file="/home/david/Pictures/software_icons/power.gif")
mButton_close.config(image=photo_power,)
mButton_close.pack(side=LEFT)



'''Volume Slider'''
vol = Scale(control_frame, orient=HORIZONTAL, length=250, from_=0.0,
            to =10.0, tickinterval=.1, command= mVolume)
vol.pack(side=RIGHT)




