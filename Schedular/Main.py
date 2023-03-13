import tkinter as tk
from tkinter import *
from tkinter import ttk
from ttkbootstrap import Style

import MStartPage
import AdminDashboard, AStudentDB, ATeacherDB, ATimetableGen, ATimetableDB
import TeacherDashboard, TTimetable
import StudentDashboard, STimetable, STodoList, STimer, SBusses

#!########################################################################
LargeFont = ('Verdana', 12)

class SchedularApp(tk.Tk):
    def __init__(self, *args, **kwargs):        
        tk.Tk.__init__(self, *args, **kwargs)
    
        style = Style()
        style.theme_use('schedulartheme')

        container = tk.Frame(self)
        container.pack(side = 'top', fill = 'both', expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}
        
        for F in (MStartPage.Page,
                    AdminDashboard.Page,
                    AStudentDB.Page,
                    ATeacherDB.Page,
                    ATimetableGen.Page,
                    ATimetableDB.Page,
                    TeacherDashboard.Page,
                    TTimetable.Page,
                    StudentDashboard.Page,
                    STimetable.Page,
                    STodoList.Page,
                    STimer.Page,
                    SBusses.Page):
            
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = 'nsew')

        self.show_frame(MStartPage.Page)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        print(f'Currently On {page} page')

if __name__ == '__main__':
    app = SchedularApp()
    app.title('Schedular')
    app.iconbitmap(r'C:\Users\Varshil Patel\OneDrive - Loughborough College\Computer Science\2. NEA CODE\SchedularVa\MainIcon.ico')
    #combo=ttk.Combobox(app)
    #combo.unbind_class("TCombobox", "<MouseWheel>")
    app.mainloop()


