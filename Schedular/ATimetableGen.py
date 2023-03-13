from cProfile import label
import tkinter as tk
from tkinter import ttk
import json

from MDBConnection import *
import ATimetableGenAlg
import AdminDashboard

#!########################################################################
LargeFont = ('Verdana', 12)

#!class of a page which runs the timetable databse management system
class Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.config_dict = {'config':{
                            'rooms':[],
                            'teachers':[],
                            }}

        #!main window of the authentication page
        self.window = tk.Frame(self)
        self.window.pack(side = 'top', fill = 'both', expand = True)
        
        #!top frame
        self.topFrame = tk.Frame(self.window)
        self.topFrame.pack(fill='x')

        #!app name in left corner of topframe
        self.logo = tk.Label(self.topFrame, text = 'Schedular > Admin Dashboard > Timetable Generation', font=LargeFont)
        self.logo.pack(padx=20, pady=10, side='left')

        #!logout button at top right corner of topframe, redirects userback to startpage
        self.backBtn = tk.Button(self.topFrame, text = 'Back to Dashboard', font=LargeFont, 
        command=lambda:self.back())
        self.backBtn.pack(padx=(5,20), pady=10, side='right')
        
        #!main frame, where the main componets of the management system reside
        self.mainFrame = tk.Frame(self.window, bg = '#2c2f33')
        self.mainFrame.pack(padx = 20, pady = 10, fill = 'both', expand = True)

        self.configFrame = tk.LabelFrame(self.mainFrame, text='Create Timetables')
        self.configFrame.grid(row=1, column=0, rowspan=3, padx=20, pady=10, sticky='nsew')

        self.resultFrame = tk.LabelFrame(self.mainFrame, text='Quick View Of Schedules Generated', height=100, width=600)
        self.resultFrame.grid(row=2, column=1, padx=20, pady=10, sticky='nsew') 

        self.infoFrame = tk.LabelFrame(self.mainFrame, text='Quick View Generation Info', height=100, width=800)
        self.infoFrame.grid(row=3, column=1, padx=20, pady=10, sticky='nsew')
        
        self.tipFrame = tk.LabelFrame(self.mainFrame, text='Tip!')
        self.tipFrame.grid(row=1, column=1, columnspan=1, padx=20, pady=10, sticky='nsew')
        self.tip = tk.Label(self.tipFrame, text='For most accurate results: - use more teachers and less rooms - atleast 2 or more rooms - atleast 2 or more teachers')
        self.tip.grid(row=1, column=1, padx=20, pady=10, sticky='w')

        self.createConfigFrame()

#!########################################################################
    def createConfigFrame(self):
        #!add room
        self.configFrame.destroy()
        self.configFrame = tk.LabelFrame(self.mainFrame, text='Create Timetables')
        self.configFrame.grid(row=1, column=0, rowspan=2, padx=20, pady=10, sticky='nsew')

        cur.execute('select * from Rooms')
        rooms = []
        for row in cur.fetchall():
            rooms.append(f'{row[1]}')

        self.roomsLbl = tk.Label(self.configFrame, text = 'Rooms')
        self.roomsLbl.grid(row = 1, column = 0, padx = 20, pady=10, sticky = 'w')
        self.roomsEntry = ttk.Combobox(self.configFrame, value = rooms, state='readonly', width = 20) 
        self.roomsEntry.current(0)
        self.roomsEntry.grid(row = 2, column = 0, padx=20, pady=(10,0), sticky = 'ew')
        self.roomsEntry.bind('<<ComboboxSelected>>', lambda e: self.addToConfig('rooms', self.roomsEntry.get(), self.roomConfigFrame))

        self.addButton = tk.Button(self.configFrame, text='Add Room',
        command=lambda:self.addToConfig('rooms', self.roomsEntry.get(), self.roomConfigFrame))
        self.addButton.grid(row=3, column=0, padx=20, pady=(0,10), sticky='ew')
        self.roomConfigFrame = tk.Frame(self.configFrame)
        self.roomConfigFrame.grid(row=4, column=0, padx=20, pady=10, sticky='nsew')

        #!add teacher
        cur.execute('select * from Teacher')
        teacherData = []
        for row in cur.fetchall():
            teacherData.append(f'{row[1]} - {row[5]}')

        self.teacherLbl = tk.Label(self.configFrame, text = 'Teachers')
        self.teacherLbl.grid(row = 1, column = 1, padx = 20, pady=10, sticky = 'w')
        self.teacherEntry = ttk.Combobox(self.configFrame, value = teacherData, state='readonly', width = 20) 
        self.teacherEntry.current(0)
        self.teacherEntry.grid(row = 2, column = 1, padx=20, pady=(10,0), sticky = 'ew')
        self.teacherEntry.bind('<<ComboboxSelected>>', lambda e: self.addToConfig('teachers', self.teacherEntry.get(), self.teacherConfigFrame))

        self.addButton = tk.Button(self.configFrame, text='Add Teacher',
        command=lambda:self.addToConfig('teachers', self.teacherEntry.get(), self.teacherConfigFrame))
        self.addButton.grid(row=3, column=1, padx=20, pady=(0,10), sticky='ew')
        self.teacherConfigFrame = tk.Frame(self.configFrame)
        self.teacherConfigFrame.grid(row=4, column=1, padx=20, pady=10, sticky='nsew') 

        #!creating/ generating new timetable, using genetic algorithm imported class
        self.createBtn = tk.Button(self.mainFrame, text = 'Create New Timetable Split?', font=LargeFont,
        command=lambda:self.createSchedules())
        self.createBtn.grid(row=3, column=0, padx = 20, pady = 0, sticky='ew')
        
        self.generationWarning = tk.Label(self.mainFrame, text='', bg='#2c2f33')
        self.generationWarning.grid(row=4, column=0, padx = 20, pady = 10, sticky='ew')

    def addToConfig(self, config, data, frame):
        if data not in self.config_dict['config'][config]:
            self.config_dict['config'][config].append(data)
            
            configDataFrame = tk.LabelFrame(frame)
            configDataFrame.pack(padx=0, pady=10, fill='x')

            delBtn = tk.Button(configDataFrame, text=' ❌ ',
            command=lambda: self.deleteConfigOption(configDataFrame, config, data))
            delBtn.grid(row=1, column=1, padx=10, pady=10)

            infoLbl = tk.Label(configDataFrame, text=data)
            infoLbl.grid(row=1, column=2, padx=(0,10), pady=10)

    def deleteConfigOption(self, configDataFrame, config, data):
        if data in self.config_dict['config'][config]:
            self.config_dict['config'][config].remove(data)
            configDataFrame.destroy()

#!########################################################################
    def createSchedules(self):
        if len(self.config_dict['config']['rooms']) >= 2:
            if len(self.config_dict['config']['teachers']) >= 2:

                with open('timetableConfig.json', 'w') as file:
                    json.dump(self.config_dict, file, indent=4)

                finalData = ATimetableGenAlg.geneticAlg().finalData

                result = finalData[0]
                clashes = finalData[1]
                accuracy = finalData[2]
                completionTime = finalData[3]

                cur.execute('''delete * from class''')
                for lesson in result:
                    conn.commit()
                    cur.execute('''insert into 
                                class(ClassroomID, SubjectName, TeacherName, Day, Period)
                                values(?,?,?,?,?)''', lesson)
                    conn.commit()

                self.generationWarning.config(text='New Timetable Split Successfully Created', fg='#7289da')
                self.createResultsFrame(result, clashes, accuracy, completionTime)
            else:
                self.generationWarning.config(text='You Need 2 or More Teachers To Make This Work', fg='red')
        else:
            self.generationWarning.config(text='You Need 2 or More Rooms To Make This Work', fg='red')

#!########################################################################
    def createResultsFrame(self, result, clashes, accuracy, completionTime):
        self.resultFrame.destroy()
        self.resultFrame = tk.LabelFrame(self.mainFrame, text='Quick View Of Schedules Generated', height=100, width=600)
        self.resultFrame.grid(row=2, column=1, padx=20, pady=10, sticky='nsew')
        
        canvas = tk.Canvas(self.resultFrame, highlightthickness=0, height=500, width=800)
        canvas.grid(row = 1, column = 1, padx = 20, pady = 10, sticky = 'nsew')
        
        self.resultClassesFrame = tk.Frame(canvas)

        scrollbar = ttk.Scrollbar(self.resultFrame, orient='vertical', command=canvas.yview)
        scrollbar.grid(row = 1, column = 2, sticky = 'ns')

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))
        self.resultClassesFrame.bind('<Enter>', lambda e: self.bindMouseWheel(e, canvas))
        self.resultClassesFrame.bind('<Leave>', lambda e: self.unbindMouseWheel(e, canvas))

        canvas.create_window((0,0), window=self.resultClassesFrame, anchor="nw")

        self.createInfoFrame(result, clashes, accuracy, completionTime)

#!########################################################################
    def createInfoFrame(self, result, clashes, accuracy, completionTime):
        self.infoFrame.destroy()
        self.infoFrame = tk.LabelFrame(self.mainFrame, text='Quick View Generation Info', height=100, width=800)
        self.infoFrame.grid(row=3, column=1, padx=20, pady=10, sticky='nsew')

        values = ['Room', 'Subject', 'Teacher', 'Day', 'Period']
        for i, lesson in enumerate(result):
            for j, detail in enumerate(lesson):
                lessonDetailLbl = tk.Label(self.resultClassesFrame, text=f'{values[j]}: {detail}')
                lessonDetailLbl.grid(row=i+1, column=j+1, padx=10, pady=10, sticky='w')

        clashesLbl = tk.Label(self.infoFrame, text=f'Number Of Classes That Clash: {clashes}')
        clashesLbl.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        accuracyLbl = tk.Label(self.infoFrame, text=f'Accuracy Of The Shceduling Algorithm: {accuracy} %')
        accuracyLbl.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        timeLbl = tk.Label(self.infoFrame, text=f'Time It Took To Generate Schedules: {completionTime} seconds')
        timeLbl.grid(row=3, column=1, padx=10, pady=10, sticky='w')

#!########################################################################
    def back(self):
        self.controller.show_frame(AdminDashboard.Page)
        for widget in self.configFrame.winfo_children():
            widget.destroy()

        for widget in self.infoFrame.winfo_children():
            widget.destroy()

        for widget in self.resultFrame.winfo_children():
            widget.destroy()

        self.generationWarning.config(text='', fg='#7289da')
        self.createConfigFrame()

#!########################################################################
    def bindMouseWheel(self, event, canvas):
        canvas.bind_all("<MouseWheel>", lambda e: self._on_mouse_wheel(e, canvas))

    def unbindMouseWheel(self, event, canvas):
        canvas.unbind_all("<MouseWheel>")

    def _on_mouse_wheel(self, event, canvas):#reduce from 120 to increase scroll speed
        canvas.yview_scroll(-1 * int((event.delta / 120)), "units")