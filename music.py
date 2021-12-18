# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 22:26:13 2021

@author: ASUS
"""
from tkinter import *
import pygame
import os
import time
class MusicPlayer:
    def __init__(self,root):
        self.root = root
        # Title of the window
        self.root.title("MusicPlayer")
        # Window Geometry
        self.root.geometry("1000x600+200+200")
        # Initiating Pygame
        pygame.init()
        # Initiating Pygame Mixer
        pygame.mixer.init()
        # Declaring track Variable
        self.track = StringVar()
        self.trackstatus = StringVar()
        self.trackstatus="Status: Playing 1:26/2:00"
        # Declaring Status Variable
        self.status = StringVar()
        self.check=-1
        self.songtracks=StringVar()
        Availsongsframe = LabelFrame(self.root,text="Available Tracks:",font=("times new roman",15,"bold"),bg="grey",fg="white",bd=5,relief=GROOVE)
        Availsongsframe.place(x=0,y=0,width=300,height=600)
        
        # Creating the Track Frames for Song label & status label
        trackframe = LabelFrame(self.root,text="Song Track",font=("times new roman",15,"bold"),bg="Navyblue",fg="white",bd=5,relief=GROOVE)
        trackframe.place(x=300,y=0,width=399,height=100)
        # Inserting Song Track Label
        songtrack = Label(trackframe,textvariable=self.track,width=20,font=("times new roman",24,"bold"),bg="Orange",fg="gold").grid(row=0,column=0,padx=8,pady=5)
        # Inserting Status Label
        trackstatus = Label(trackframe,textvariable=self.status,font=("times new roman",24,"bold"),bg="orange",fg="gold").grid(row=0,column=1,padx=10,pady=5)
    
        # Creating Button Frame
        buttonframe = LabelFrame(self.root,text="Control Panel",font=("times new roman",15,"bold"),bg="grey",fg="white",bd=5,relief=GROOVE)
        buttonframe.place(x=300,y=100,width=400,height=500)
        
        addbtn = Button(buttonframe,text="Add >",command=self.addsong,width=12,height=1,font=("times new roman",14,"bold"),fg="black",bg="green").grid(row=0,column=0,padx=10,pady=5)
        removebtn = Button(buttonframe,text="< Remove",command=self.removesong,width=12,height=1,font=("times new roman",14,"bold"),fg="black",bg="green").grid(row=1,column=0,padx=10,pady=5)
        removeallbtn = Button(buttonframe,text="<< Remove All",command=self.removeallsong,width=12,height=1,font=("times new roman",14,"bold"),fg="black",bg="green").grid(row=2,column=0,padx=10,pady=5)
        
        # Inserting Play Button
        playbtn = Button(buttonframe,text="Play",command=self.playsong,width=12,height=1,font=("times new roman",14,"bold"),fg="black",bg="green").grid(row=3,column=0,padx=10,pady=5)
        # Inserting Pause Button
        playbtn = Button(buttonframe,text="Pause",command=self.pausesong,width=12,height=1,font=("times new roman",14,"bold"),fg="black",bg="green").grid(row=4,column=0,padx=150,pady=5)
        # Inserting Stop Button
        playbtn = Button(buttonframe,text="Stop",command=self.stopsong,width=12,height=1,font=("times new roman",14,"bold"),fg="black",bg="green").grid(row=5,column=0,padx=10,pady=5)
        Label(buttonframe, text = "Volume:",width=12,height=1,font=("times new roman",14),fg="black",bg="grey").grid(row=6,column=0,padx=10,pady=5)
        self.vol = Scale(buttonframe,from_ = 0,to = 100,orient = HORIZONTAL ,resolution = 1,command=self.change_vol,width=10,bd=10,bg="grey", variable=100,length=220)
        self.vol.set(100)
        self.vol.grid(row=7,column=0,padx=10,pady=5)
        # Creating Playlist Frame
        pygame.mixer.music.set_volume(100)
        
        SelectedSongsframe = LabelFrame(self.root,text="Selected Tracks:",font=("times new roman",15,"bold"),bg="grey",fg="white",bd=5,relief=GROOVE)
        SelectedSongsframe.place(x=700,y=0,width=300,height=600)
        self.labelbtn=Label(self.root, text='',width=20,height=1,font=("times new roman",14),fg="black",bg="grey")
        self.labelbtn.place(x=750,y=300)
        self.songslider= Scale(self.root ,from_ = 0,to = 100,orient = HORIZONTAL ,resolution = 1,command=self.seekbar,width=10,bd=10,bg="grey",length=220)
        self.songslider.set(0)
        self.songslider.place(x=720,y=340)
        # Inserting scrollbar
        scrol_y = Scrollbar(Availsongsframe,orient=VERTICAL)
        # Inserting Playlist listbox
        self.playlist = Listbox(Availsongsframe,yscrollcommand=scrol_y.set,selectbackground="gold",selectmode=SINGLE,font=("times new roman",12,"bold"),bg="silver",fg="navyblue",bd=5,relief=GROOVE)
        # Applying Scrollbar to listbox
        scrol_y.pack(side=RIGHT,fill=Y)
        scrol_y.config(command=self.playlist.yview)
        self.playlist.pack(fill=BOTH)
        
        # Inserting scrollbar
        scrol_y2 = Scrollbar(SelectedSongsframe,orient=VERTICAL)
        # Inserting Playlist listbox
        self.playlist2 = Listbox(SelectedSongsframe,yscrollcommand=scrol_y2.set,selectbackground="gold",selectmode=SINGLE,font=("times new roman",12,"bold"),bg="silver",fg="navyblue",bd=5,relief=GROOVE)
        # Applying Scrollbar to listbox
        scrol_y2.pack(side=RIGHT,fill=Y)
        scrol_y2.config(command=self.playlist2.yview)
        self.playlist2.pack(fill=BOTH)
        
        # Changing Directory for fetching Songs
        os.chdir("D:/OneDrive - Indian Institute of Technology Guwahati/Project/tutorpoint2/music")
        # Fetching Songs
        songtracksAll = os.listdir()
        # Inserting Songs into Playlist
        self.songtracks = list(filter(lambda f: f.endswith('.mp3'), songtracksAll))
        for track in self.songtracks:
          self.playlist.insert(END,track)
          
    def play_time(self):
        song_length=pygame.mixer.Sound(self.playlist2.get(ACTIVE)).get_length()
        conv_time=time.strftime('%H:%M:%S',time.gmtime(song_length))
        if pygame.mixer.music.get_pos()==-1:
            self.labelbtn.config(text='Status: Stopped 0.00 s')
            self.songslider.set(0)
            return 
        elif pygame.mixer.music.get_pos()==song_length:
            self.labelbtn.config(text='Status: Stopped'+str(conv_time)+'s')
            self.songslider.set(song_length)
            return 
        else:
            current_time=int(pygame.mixer.music.get_pos())/1000
            conv_time=time.strftime('%H:%M:%S',time.gmtime(current_time))    
            self.labelbtn.config(text='Status: Playing '+str(conv_time)+'s')
            self.songslider.set(current_time)
        self.labelbtn.after(1000,self.play_time)
            
    def seekbar(self,loc):
        if self.check!=1:
            return
        #self.songslider.set(current_time)
        #pygame.mixer.music.set_pos(loc)
        #pygame.mixer.music.play(loops=0, start=int(self.songslider.get()))
        
        pass
    def addsong(self):
        if self.playlist.size()==0:
            return
        self.track.set(self.playlist.get(ACTIVE))
        self.playlist2.insert(END,self.playlist.get(ACTIVE))
        
    def removesong(self):
        if self.playlist2.size()==0:
            return
        idx = self.playlist2.get(0, END).index(self.playlist2.get(ACTIVE))
        self.playlist2.delete(idx)
        
    def removeallsong(self):
        if self.playlist2.size()==0:
            return
        self.playlist2.delete(0, END)
        
    def change_vol(self,vol):
        if self.check!=1:
            return
        vol=int(vol)
        pygame.mixer.music.set_volume(vol)
        
    def playsong(self):
        if self.playlist2.size()==0:
            return
        # Displaying Selected Song title
        self.track.set(self.playlist2.get(ACTIVE))
        if self.check==1:
            return
        elif self.check==0:
            self.status.set("-Playing")
            pygame.mixer.music.unpause()
            self.check=1
        else:
            self.check=1
            # Displaying Status
            self.status.set("-Playing")
            # Loading Selected Song
            pygame.mixer.music.load(self.playlist2.get(ACTIVE))
            
            # Playing Selected Song
            #pygame.mixer.music.play()
            pygame.mixer.music.play(loops=0, start=int(self.songslider.get()))
        song_length=pygame.mixer.Sound(self.playlist2.get(ACTIVE)).get_length()
        self.songslider.config(to=int(song_length))
        self.play_time()
    def stopsong(self):
        if self.playlist2.size()==0:
            return
        if self.check==2:
            return
        # Displaying Status
        current_time=int(pygame.mixer.music.get_pos())/1000
        conv_time=time.strftime('%H:%M:%S',time.gmtime(current_time))    
        self.labelbtn.config(text='Status: Stopped '+str(conv_time)+'s')
        self.songslider.set(current_time)
        
        self.status.set("-Stopped")
        # Stopped Song
        pygame.mixer.music.stop()
        self.check=2
    
    def pausesong(self):
        if self.playlist2.size()==0:
            return
        # Displaying Status
        if self.check==0:
            return
        current_time=int(pygame.mixer.music.get_pos())/1000
        conv_time=time.strftime('%H:%M:%S',time.gmtime(current_time))    
        self.labelbtn.config(text='Status: Paused '+str(conv_time)+'s')
        self.songslider.set(current_time)
        self.status.set("-Paused")
        # Paused Song
        pygame.mixer.music.pause()
        self.check=0
    

root = Tk()
MusicPlayer(root)

root.mainloop()