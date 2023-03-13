import tkinter as tk
from tkinter.font import Font

import MData
import StudentDashboard
import TeacherDashboard

#!################################################################################################
LargeFont = ('Verdana', 12)

class Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.clockFont = Font(
            family='Arial Rounded MT Bold',
            size=75,
            underline=1,
            overstrike=0
        )

        self.controller = controller

        self.window = tk.Frame(self)
        self.window.pack(side = 'top', fill = 'both', expand = True)

        self.topFrame = tk.Frame(self.window)
        self.topFrame.pack(fill='x')

        self.logo = tk.Label(self.topFrame, text = 'Schedular > Pomodoro Timer', font=LargeFont)
        self.logo.pack(padx=20, pady=10, side='left')

        self.backBtn = tk.Button(self.topFrame, text = 'Back to Dashboard', font=LargeFont, 
        command=lambda:self.back())
        self.backBtn.pack(padx=(5,20), pady=10, side='right')

        self.mainFrame = tk.Frame(self.window, bg = '#2c2f33')
        self.mainFrame.pack(padx = 20, pady = 10, fill = 'both', expand = True)

        self.timerFunc()
#!################################################################################################
    def back(self):
        page = StudentDashboard.Page if MData.userType == 'Student' else TeacherDashboard.Page
        self.controller.show_frame(page)

        self.stop()
        self.setTime(sec=25*60)

#!################################################################################################
    def timerFunc(self):
        self.timeSec = 0
        self.running = False
        self.clockType = ''
        #!######
        self.timerFrame = tk.Frame(self.mainFrame)
        self.timerFrame.pack(padx=20, pady=10)

        self.timerConfigFrame = tk.Frame(self.timerFrame)
        self.timerConfigFrame.grid(row=1, column=1, padx=20, pady=10, sticky='ew')

        self.pomodoroBtn = tk.Button(self.timerConfigFrame, text='Pomodoro',
        command=lambda: [self.setTime(sec=25*60), self.setTitle('Pomodoro'), self.stop()])
        self.pomodoroBtn.grid(row=1, column=1, padx=20, pady=10, sticky='ew')

        self.shortBreakBtn = tk.Button(self.timerConfigFrame, text='Short Break',
        command=lambda: [self.setTime(sec=5*60), self.setTitle('Short Break'), self.stop()])
        self.shortBreakBtn.grid(row=1, column=2, padx=20, pady=10, sticky='ew')

        self.longBreakBtn = tk.Button(self.timerConfigFrame, text='Long Break',
        command=lambda: [self.setTime(sec=15*60), self.setTitle('Long Break'), self.stop()])
        self.longBreakBtn.grid(row=1, column=3, padx=20, pady=10, sticky='ew')

        self.customBtn = tk.Button(self.timerConfigFrame, text='Custom Timer',
        command=lambda: [self.setTitle('Custom Timer'), self.custom()])
        self.customBtn.grid(row=1, column=4, padx=20, pady=10, sticky='ew')

        #!######
        self.timerClockFrame = tk.Frame(self.timerFrame)
        self.timerClockFrame.grid(row=2, column=1, padx=20, pady=10)
        
        self.title = tk.Label(self.timerClockFrame, text='')
        self.title.pack(padx=20, pady=(5,0))

        self.timerClock = tk.Label(self.timerClockFrame, text='', font=self.clockFont)
        self.timerClock.pack(padx=20, pady=10)
        self.setTime(sec=25*60)
        self.setTitle('Pomodoro')

        self.startStopToggle= tk.Button(self.timerClockFrame, text='Start',
        command=lambda:self.start())
        self.startStopToggle.pack(padx=20, pady=10, fill='x')

#!################################################################################################
    def setTitle(self, title):
        self.title.config(text=title)

#!################################################################################################
    def setTime(self, sec):
        self.timeSec = sec
        min, sec = divmod(sec, 60)
        hrs, min = divmod(min, 60)

        clock = str(hrs).zfill(2) + ':' + str(min).zfill(2) + ':' + str(sec).zfill(2)
        self.timerClock.config(text=clock, fg='#7289da')

    def timer(self):
        if self.running == True:
            if self.timeSec <= 0:
                self.timerClock.config(fg='#d95550')
                self.running = False
            else:
                self.timeSec -= 1
                self.setTime(self.timeSec)
                self.after(1, self.timer)

#!################################################################################################
    def start(self):
        self.running = True
        self.startStopToggle.config(text='Stop', command=lambda: self.stop())
        self.timer()

    def stop(self):
        self.running = False
        self.startStopToggle.config(text='Start', command=lambda: self.start())
        self.timer()

#!################################################################################################
    def custom(self):
        popup = tk.Toplevel(self)
        popup.title('Set Custom Timer')
        popup.config(bg='#23272a')
        
        popup.focus_set()
        popup.grab_set()

        popupFrame = tk.LabelFrame(popup)
        popupFrame.pack(padx=10, pady=10)

        hrsLbl = tk.Label(popupFrame, text='Hours:', bg='#23272a', fg='#7289da')
        hrsLbl.grid(row=1, column=1, padx=10, pady=10)
        hrsEntry = tk.Entry(popupFrame)
        hrsEntry.grid(row=2, column=1, padx=10, pady=10)
        hrsEntry.focus()

        minLbl = tk.Label(popupFrame, text='Minutes:', bg='#23272a', fg='#7289da')
        minLbl.grid(row=1, column=2, padx=10, pady=10)
        minEntry = tk.Entry(popupFrame)
        minEntry.grid(row=2, column=2, padx=10, pady=10)
        minEntry.focus()

        secLbl = tk.Label(popupFrame, text='Seconds:', bg='#23272a', fg='#7289da')
        secLbl.grid(row=1, column=3, padx=10, pady=10)
        secEntry = tk.Entry(popupFrame)
        secEntry.grid(row=2, column=3, padx=10, pady=10)
        secEntry.focus()
        
        submitBtn = tk.Button(popupFrame, text='Submit', bg='#7289da',
        command=lambda:self.setCustomTime(hrsEntry.get(), minEntry.get(), secEntry.get(), popup))
        submitBtn.grid(row=3, column=1, columnspan=3, padx=10, pady=10, sticky='ew')

        self.setTimerWarning = tk.Label(popupFrame, text='', bg='#23272a')
        
        popup.mainloop()

    def setCustomTime(self, hrs, min, sec, popup):
        if hrs != '' or min != '' or sec != '':
            if hrs.isdigit() and min.isdigit() and sec.isdigit():
                hrs_to_sec = int(hrs)*60*60
                min_to_sec = int(min)*60
                sec_to_sec = int(sec)
                sec = hrs_to_sec + min_to_sec + sec_to_sec
                self.setTime(sec)

                self.setTimerWarning.config(text='Successfully Set Custom Time', fg='#7289da')
                popup.destroy()
            else:
                self.setTimerWarning.config(text='Time Must Be Integer', fg='red')
                self.setTimerWarning.grid(row=4, column=1, columnspan=3, padx=10, pady=10, sticky='ew')
        else:
            self.setTimerWarning.config(text='Fields Must Be Filled', fg='red')
            self.setTimerWarning.grid(row=4, column=1, columnspan=3, padx=10, pady=10, sticky='ew')