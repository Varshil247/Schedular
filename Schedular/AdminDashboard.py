import tkinter as tk
from tkcalendar import *

import MData
import MStartPage
import AStudentDB
import ATeacherDB
import ATimetableGen
import ATimetableDB

#!########################################################################
LargeFont = ('Verdana', 12)

#!class of a page which displays the dashboard of admin user
class Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        #!main window of the admin dashboard page
        self.window = tk.Frame(self)
        self.window.pack(side = 'top', fill = 'both', expand = True)

        #!top frame
        self.topFrame = tk.Frame(self.window)
        self.topFrame.pack(fill='x')

        #!app name in left corner of topframe
        self.logo = tk.Label(self.topFrame, text = 'Schedular > Admin Dashboard', font=LargeFont)
        self.logo.pack(padx=20, pady=10, side='left')
        
        #!logout button at top right corner of topframe, redirects userback to startpage
        self.logoutBtn = tk.Button(self.topFrame, text = 'Logout', font=LargeFont, command=lambda:[self.logout()])
        self.logoutBtn.pack(padx=(5,20), pady=10, side='right')

        #!dashboard frame where there are buttons/ links to feature pages
        self.mainFrame = tk.Frame(self.window, bg = '#2c2f33')
        self.mainFrame.pack(padx=20, pady=30)

        #!label greeting admin users to the dashboard
        self.titleLbl = tk.Label(self.mainFrame, text = f'Welcome To The Admin Dashboard', bg = '#2c2f33')
        self.titleLbl.pack(padx = 20, pady = 10, fill = 'both', expand = True)

        #!button that redirects to student database management system
        self.studentDBPageBtn = tk.Button(self.mainFrame, text = 'Manage Students', height = 2,
        command = lambda: self.controller.show_frame(AStudentDB.Page))
        self.studentDBPageBtn.pack(padx = 20, pady = 10, fill = 'both', expand = True)

        #!button that redirects to teacher database management system
        self.teacherDBPageBtn = tk.Button(self.mainFrame, text = 'Manage Teachers', height = 2, width=40,
        command = lambda: self.controller.show_frame(ATeacherDB.Page))
        self.teacherDBPageBtn.pack(padx = 20, pady = 10, fill = 'both', expand = True)
        
        #!button that redirects to timetable database management system, and generation page
        self.timetableGenPageBtn = tk.Button(self.mainFrame, text = 'Generate Timetables', height = 2,
        command = lambda: self.controller.show_frame(ATimetableGen.Page))
        self.timetableGenPageBtn.pack(padx = 20, pady = 10, fill = 'both', expand = True)

        self.timetableDBPageBtn = tk.Button(self.mainFrame, text = 'Manage Timetables', height = 2,
        command = lambda: self.controller.show_frame(ATimetableDB.Page))
        self.timetableDBPageBtn.pack(padx = 20, pady = 10, fill = 'both', expand = True)

        #return('admin dashboard initialized')

    #!function that logs users out of app and back to startpage
    def logout(self):
        self.controller.show_frame(MStartPage.Page)
        print(MData.username, MData.userType, 'Logged Out')
        return(MData.username, MData.userType, 'Logged Out')