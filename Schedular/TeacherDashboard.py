import tkinter as tk
from tkcalendar import *

import MData
import MStartPage
import TTimetable
import STodoList
import STimer
import SBusses

#!########################################################################
LargeFont = ('Verdana', 12)

class Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.window = tk.Frame(self)
        self.window.pack(side = 'top', fill = 'both', expand = True)
        
        self.topFrame = tk.Frame(self.window)
        self.topFrame.pack(fill='x')

        self.logo = tk.Label(self.topFrame, text = 'Schedular > Teacher Dashboard', font=LargeFont)
        self.logo.pack(padx=20, pady=10, side='left')

        self.logoutBtn = tk.Button(self.topFrame, text = 'Logout', font=LargeFont, command=lambda:[self.logout()])
        self.logoutBtn.pack(padx=(5,20), pady=10, side='right')

        self.mainFrame = tk.Frame(self.window, bg = '#2c2f33')
        self.mainFrame.pack(padx = 20, pady = 30)

        self.titleLbl = tk.Label(self.mainFrame, text = f'WELCOME TO THE TEACHER DASHBOARD', bg = '#2c2f33')
        self.titleLbl.pack(padx = 20, pady = 10, fill = 'both', expand = True)

        self.timetablePageBtn = tk.Button(self.mainFrame, text = 'TIMETABLE', height = 2, width=40,
        command = lambda: self.controller.show_frame(TTimetable.Page))
        self.timetablePageBtn.pack(padx = 20, pady = 10, fill = 'both', expand = True)

        self.todoPageBtn = tk.Button(self.mainFrame, text = 'TODO', height = 2, 
        command = lambda: self.controller.show_frame(STodoList.Page))
        self.todoPageBtn.pack(padx = 20, pady = 10, fill = 'both', expand = True)

        self.pomoTimerPageBtn = tk.Button(self.mainFrame, text = 'POMO', height = 2, 
        command = lambda: self.controller.show_frame(STimer.Page))
        self.pomoTimerPageBtn.pack(padx = 20, pady = 10, fill = 'both', expand = True)

        self.bussesPageBtn = tk.Button(self.mainFrame, text = 'BUSSES', height = 2, 
        command = lambda: self.controller.show_frame(SBusses.Page))
        self.bussesPageBtn.pack(padx = 20, pady = (10,20), fill = 'both', expand = True)

        #return('teacher dashboard initialized')

    def logout(self):
        self.controller.show_frame(MStartPage.Page)
        print(MData.username, MData.userType, 'Logged Out')
        return(MData.username, MData.userType, 'Logged Out')