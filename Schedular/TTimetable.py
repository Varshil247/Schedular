import tkinter as tk
import json

from MDBConnection import *
import MData
import TeacherDashboard
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

        self.logo = tk.Label(self.topFrame, text = 'Schedular > Teacher Dashboard > Your Schedules', font=LargeFont)
        self.logo.pack(padx=20, pady=10, side='left')

        self.backBtn = tk.Button(self.topFrame, text = 'Back to Dashboard', font=LargeFont, 
        command=lambda:self.back())
        self.backBtn.pack(padx=(5,20), pady=10, side='right')

        self.mainFrame = tk.Frame(self.window, bg = '#2c2f33')
        self.mainFrame.pack(padx = 20, pady = 10, fill = 'both', expand = True)

        self.chooseScheduleFrame = tk.LabelFrame(self.mainFrame, text='Choose which timetable you want to view.')
        self.chooseScheduleFrame.grid(row=1 ,column=1, padx=20, pady=10, sticky='w')

        self.btn2 = tk.Button(self.chooseScheduleFrame, text = 'Show school timetable', 
        command = lambda: [self.showSchoolTable(), self.showSchoolSchedule(teacherName=MData.username)])
        self.btn2.grid(row=1, column=1, padx=20, pady=10, sticky='w')
        
        self.btn3 = tk.Button(self.chooseScheduleFrame, text = 'Show home timetable', 
        command = lambda: [self.showHomeTable(), self.showHomeSchedule(teacherName=MData.username)])
        self.btn3.grid(row=1, column=2, padx=20, pady=10, sticky='w')

        self.timetableFrame = tk.Frame(self.mainFrame, bg = '#2c2f33')
        self.timetableFrame.grid(row=2, column=1, padx=20, pady=10)

#!########################################################################
    def showSchoolTable(self):
        self.schoolTimetable = tk.LabelFrame(self.timetableFrame, text='School Schedule', background='#23272a', width=100, height=100)
        self.schoolTimetable.grid(row=1, column=1, columnspan=(100), padx = 20, pady = 10, sticky='nsew')

        days=['Monday','Tuesday','Wednesday','Thursday','Friday']
        periods=['Period 1\n09:00 - 10:00','Period 2\n10:00 - 11:00','Period 3\n11:00 - 12:00','Period 4\n12:00 - 13:00','Period 5\n13:00 - 14:00']

        for i in range (5):
            self.dayLbl = tk.Label(self.schoolTimetable, text=days[i])
            self.dayLbl.grid(row=0, column=i+1, padx=5, pady=5)

            self.periodLbl = tk.Label(self.schoolTimetable, text=periods[i])
            self.periodLbl.grid(row=i+1, column=0, padx=5, pady=5)

        for i in range(5):
            for j in range(5):
                self.lessonFrame = tk.LabelFrame(self.schoolTimetable, background='black', width=150, height=75)
                self.lessonFrame.grid(row=i+1, column=j+1, padx=5, pady=5)


    def showSchoolSchedule(self, teacherName):
        cur.execute('SELECT * FROM Class WHERE TeacherName = ?', teacherName)
        for row in (cur.fetchall()):
            self.lessonLbl = tk.Label(self.schoolTimetable, text=row[1]+'\n'+row[2]+'\n'+row[3], background='black')
            self.lessonLbl.grid(row=row[5], column=row[4], padx=5, pady=5)
        #print('welp your a studnet, feature yet to be added')

#!########################################################################
    def showHomeTable(self):
        self.homeTimetable = tk.LabelFrame(self.timetableFrame, text='Home Schedule', background='#23272a', width=100, height=100)
        self.homeTimetable.grid(row=1, column=1, columnspan=(100), padx = 20, pady = 10, sticky='nsew')

        days=['Monday','Tuesday','Wednesday','Thursday','Friday']
        periods=['Period 1\n15:00 - 16:00','Period 2\n17:00 - 18:00','Period 3\n19:00 - 20:00','Period 4\n21:00 - 22:00','Period 5\n23:00 - 24:00']
    
        for i in range (5):
            self.dayLbl = tk.Label(self.homeTimetable, text=days[i])
            self.dayLbl.grid(row=0, column=i+1, padx=5, pady=5)

            self.periodLbl = tk.Label(self.homeTimetable, text=periods[i])
            self.periodLbl.grid(row=i+1, column=0, padx=5, pady=5)

        self.timeSlotList=[]
        for i in range(5):
            self.timeSlotList.append([])
            for j in range(5):
                self.timeSlotList[i].append([])

                self.timeSlot = tk.Text(self.homeTimetable, background='black', fg='white', width=20, height=3, insertbackground='white')
                self.timeSlot.grid(row=i+1, column=j+1, padx=5, pady=5)
                self.timeSlot.insert('insert', '')
                
                self.timeSlotList[i][j].append(j+1)
                self.timeSlotList[i][j].append(i+1)
                self.timeSlotList[i][j].append(self.timeSlot)

        self.updateBtn = tk.Button(self.homeTimetable, text='Update Your Home Schedule',
        command=lambda:self.updateHomeSchedule())
        self.updateBtn.grid(row=10, column=0, columnspan=10, padx=20, pady=10, sticky='ew')

    def showHomeSchedule(self, teacherName):
        cur.execute('SELECT * FROM HomeSchedules WHERE Username = ? and Usertype = ?', teacherName, 'Teacher')
        for row in (cur.fetchall()):
            for timeSlots in self.timeSlotList:
                for timeSlot in timeSlots:
                    day = timeSlot[0]
                    period = timeSlot[1]
                    if int(row[4]) == int(day) and int(row[5]) == int(period):
                        timeSlot[2].insert('insert', row[3])
            

    def updateHomeSchedule(self):
        cur.execute('''DELETE * FROM HomeSchedules WHERE username=? and usertype=?''', MData.username, MData.userType)
        cur.commit()
        for timeSlots in self.timeSlotList:
            for timeSlot in timeSlots:
                day = timeSlot[0]
                period = timeSlot[1]
                info = timeSlot[2].get('1.0','end-1c')
               
                newSlot = (MData.username, MData.userType, info, day, period)
                if str(info) != '':
                    print(newSlot)
                    cur.execute('''INSERT INTO
                                HomeSchedules(username, usertype, info, day, period) 
                                Values(?,?,?,?,?)''', newSlot)
                    conn.commit()

#!########################################################################
    def back(self):
        self.controller.show_frame(TeacherDashboard.Page)
        for widget in self.timetableFrame.winfo_children():
            widget.destroy()
        
        self.timetableFrame = tk.Frame(self.mainFrame, bg = '#2c2f33')
        self.timetableFrame.grid(row=2, column=1, padx = 20, pady = 10)
