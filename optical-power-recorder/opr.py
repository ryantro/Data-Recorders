# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 11:05:00 2022

@author: ryan.robinson
"""

# IMPORTS
import tkinter as tk
import threading
import time
import numpy as np

class Application:
    def __init__(self, master):
        """ CREATE THE PROGRAM GUI """
        
        # APPLICATION MASTER FRAME
        self.master = master
        
        # ON APPLICAITON CLOSING
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # BOX CONFIGURE
        self.master.title('O.P.R. - Optical Power Recorder')
        
        # DEFINE RUNFRAME
        self.runframe = tk.Frame(self.master)
        self.runframe.rowconfigure([0, 1], minsize=30, weight=1)
        self.runframe.columnconfigure([0, 1], minsize=25, weight=1)

        # ENTRY LABEL
        self.entryLabel = tk.Label(self.runframe,text="Save file:", font = ('Ariel 15'))
        self.entryLabel.grid(row=0, column=0, sticky = "W", padx = 10)
        
        # ENTRY BOX
        self.entry = tk.Entry(self.runframe, text = 'Entry', width = 60, font = ('Ariel 15'))
        self.entry.grid(row = 0, column = 1, sticky = "W", padx = (0,10), pady = 10)
        self.entry.insert(0, r'record-folder/test-data.py')

        # GENERATE STATION ENABLE BOX
        self.stateframe = tk.Frame(self.runframe, borderwidth = 2,relief="groove")
        self.stateframe.columnconfigure([0, 1], minsize=50, weight=1)
        self.stateframe.rowconfigure([0], minsize=50, weight=1)
        self.stateframe.grid(row = 1, column = 0, columnspan = 2, padx = 10, pady = (0,10), sticky = "EW")
        
        # GENERATE ENABLE/DISABLE BUTTON
        self.stateButton = tk.Button(self.stateframe, text="START", command=self.stateToggle, font = ('Ariel 15'))
        self.stateButton.grid(row = 0, column = 0, padx = 0, pady = 0, sticky = "NSEW")
        
        # GENERATE STATION STATUS BOX
        self.statelabel = tk.Label(self.stateframe, text=" RECORDING OFF ", bg = '#84e47e', font = ('Ariel 15'))
        self.statelabel.grid(row = 0, column = 1, padx = 0, pady = 0, sticky = "NSEW")

        # VARIABLES
        self.recording = False
        
        # THREADS
        self.recordThread = threading.Thread(target = self.record)
        
        # FRAME PACKING
        self.runframe.pack()
        
        return

    def stateToggle(self):
        """ TOGGLE THE STATE """
        
        # IF IT CURRENTLY NOT RECORDING, START RECORDING
        if(self.recording == False):
            
            # DISABLE ENTRY BOX
            self.entry.configure(state = 'disabled')
            
            # SET GRID LOCAITONS OF BUTTONS AND LABELS
            self.statelabel.grid(row = 0, column = 0, padx = 0, pady = 0, sticky = "NSEW")
            self.stateButton.grid(row = 0, column = 1, padx = 0, pady = 0, sticky = "NSEW")
            
            # CONFIGURE BUTTON AND LABEL TEXT
            self.stateButton.configure(text = "STOP")
            self.statelabel.configure(text = "CURRENTLY RECORDING", bg = '#F55e65')
            
            # SET RECORDING STATE TO TRUE
            self.recording = True
            
            # START THE THREAD IF IT CURRENTLY ISN'T ALIVE
            if(self.recordThread.is_alive() == False):
                
                # CREATE THE THREAD
                self.recordThread = threading.Thread(target = self.record)
                
                # START THE THREAD
                self.recordThread.start()
        
        # IF IT IS CURRENTLY RECORDING, STOP THE RECORDING
        else:
            # ENABLE ENTRY BOX
            self.entry.configure(state = 'normal')
            
            # SET GRID LOCATIONS OF BUTTONS AND LABELS
            self.statelabel.grid(row = 0, column = 1, padx = 0, pady = 0, sticky = "NSEW")
            self.stateButton.grid(row = 0, column = 0, padx = 0, pady = 0, sticky = "NSEW")
            
            # CONFIGURE BUTTON AND LABEL TEXT
            self.stateButton.configure(text = "START")
            self.statelabel.configure(text=" RECORDING OFF ", bg = '#84e47e', font = ('Ariel 15'))
            
            # SET RECORDING STATE TO FALSE
            self.recording = False
        
        return

    def record(self):
        """ RECORD DATA FROM THE POWER METER """
        
        # RECORD DATA WHILE RECORDING
        while(self.recording):
            print("time: {}".format(time.time()))
            time.sleep(0.5)
        
        return
    
    def on_closing(self):
        """ EXIT THE APPLICATION """
        
        # PROMPT DIALOG BOX
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            
            # SET RECORDING TO FALSE
            self.recording = False
            
            # JOIN THE THREAD IF IT IS ALIVE
            if(self.recordThread.is_alive() == True):
                self.recordThread.join(10)
            
            # DESTROY APPLICATION
            self.master.destroy()
            
        return








def main():
    """ MAIN THREAD """
    # CREATE ROOT TKINTER OBJECT
    root = tk.Tk()
    
    # CREATE APPLICATION
    app = Application(root)
    
    # RUN MAINLOOP
    root.mainloop()
    
    return



if __name__=="__main__":
    main()