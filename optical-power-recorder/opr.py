# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 11:05:00 2022

@author: ryan.robinson
"""

# IMPORTS
import tkinter as tk
from tkinter import ttk
import threading
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

# FOR UNIT TESTING
import random

# POWER METER
import power_meter

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
        self.runframe.rowconfigure([0, 1, 2, 3], minsize=30, weight=1)
        self.runframe.columnconfigure([0, 1], minsize=25, weight=1)

        # ENTRY LABEL
        self.entryLabel = tk.Label(self.runframe,text="Save file:", font = ('Ariel 15'))
        self.entryLabel.grid(row=0, column=0, sticky = "W", padx = 10)
        
        # ENTRY BOX
        self.entry = tk.Entry(self.runframe, text = 'Entry', width = 60, font = ('Ariel 15'))
        self.entry.grid(row = 0, column = 1, sticky = "W", padx = (0,10), pady = 10)
        self.entry.insert(0, r'record-folder/test-data.py')

        # LATEST MEASUREMENT LABEL
        self.measurementLabel = tk.Label(self.runframe, text = "Power:", font = ('Ariel 15'))
        self.measurementLabel.grid(row=1, column=0, sticky = "W", padx = 10)
        
        # LASEST MEASUREMENT
        recentMeasurement = "{:.4f} mW".format(0)
        self.var = tk.StringVar(self.runframe, value = recentMeasurement)
        self.measurement = tk.Label(self.runframe, textvariable = self.var, font = ('Ariel 15'))
        self.measurement.grid(row=1, column=1, sticky = "W", padx = (0,10))

        # GENERATE STATION ENABLE BOX
        self.stateframe = tk.Frame(self.runframe, borderwidth = 2,relief="groove")
        self.stateframe.columnconfigure([0, 1], minsize=50, weight=1)
        self.stateframe.rowconfigure([0], minsize=50, weight=1)
        self.stateframe.grid(row = 3, column = 0, columnspan = 2, padx = 10, pady = (0,10), sticky = "EW")
        
        # GENERATE ENABLE/DISABLE BUTTON
        self.stateButton = tk.Button(self.stateframe, text="START", command=self.stateToggle, font = ('Ariel 15'))
        self.stateButton.grid(row = 0, column = 0, padx = 0, pady = 0, sticky = "NSEW")
        
        # GENERATE STATION STATUS BOX
        self.statelabel = tk.Label(self.stateframe, text=" RECORDING OFF ", bg = '#84e47e', font = ('Ariel 15'))
        self.statelabel.grid(row = 0, column = 1, padx = 0, pady = 0, sticky = "NSEW")

        # VARIABLES
        self.recording = False
        self.tList = []
        self.pList = []
        
        # GENERATE PLOT
        # bg = self.runframe.cget('background')
        
        fig = plt.figure()
        fig.set_facecolor('#f0f0f0')
 
        
        self.powerPlot = fig.add_subplot(111)
        self.powerPlot.set_title("Power")
        self.powerPlot.set_ylabel("Power (mW)", fontsize = 14)
        self.powerPlot.set_xlabel("Time (s)", fontsize = 14)
        self.powerPlot.grid('On')
        self.canvas = FigureCanvasTkAgg(fig, master = self.runframe)
        self.canvas.get_tk_widget().grid(row=2, column=0, columnspan=2, ipadx=60, ipady=20, sticky = "EW", padx = 10, pady = (0,10))
        self.canvas.draw()

        plt.close(fig)
        
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
        
        try:
            PM = power_meter.PowerMeter()
        
        
            # CLEAR LISTS
            self.tList = []
            self.pList = []
            
            # CONFIGURE PLOT
            self.powerPlot.cla()
            self.powerPlot.set_title("Power")
            self.powerPlot.set_ylabel("Power (mW)", fontsize = 14)
            self.powerPlot.set_xlabel("Time (s)", fontsize = 14)
            self.powerPlot.grid('On')
            
            # MARK START TIME
            startTime = time.time()
            
            # RECORD DATA WHILE RECORDING
            while(self.recording):
                print("time: {}".format(time.time()))
                
                # UPDATE THE MOST RECENT VALUE
                # recentVal = random.random()
                recentVal = PM.getPower2()
                print(recentVal)
                self.var.set("{:.4f} mW".format(recentVal))
                
                # APPEND VALUES TO LISTS
                self.tList.append(time.time())
                self.pList.append(recentVal)
                
                # UPDATE THE PLOTS
                # self.powerPlot.clear()
                if(len(self.tList) > 1):
                    self.powerPlot.plot([self.tList[-2] - startTime, self.tList[-1] - startTime], [self.pList[-2], self.pList[-1]], color = 'orange') #self.tList, self.pList)
                
                # self.powerPlot.set_data([],[])
                
                self.canvas.draw_idle()
                
                """
                TODO
                    Append data to a csv
                
                """
                # SLEEP
                time.sleep(1)
        
        finally:
            
            # CLOSE DEVICE
            PM.close()
        
        return
    
    def on_closing(self):
        """ EXIT THE APPLICATION """
        
        # PROMPT DIALOG BOX
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            
            # SET RECORDING TO FALSE
            self.recording = False
            
            # JOIN THE THREAD IF IT IS ALIVE
            if(self.recordThread.is_alive() == True):
                self.recordThread.join(2)
            
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