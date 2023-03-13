import tkinter as tk
from tkinter import ttk
from tkinter.constants import CENTER, NO, RIGHT

from MDBConnection import *
import AdminDashboard

#!########################################################################
LargeFont = ('Verdana', 12)

#!class of a page which runs the timetable databse management system
class Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        #!main window of the authentication page
        self.window = tk.Frame(self)
        self.window.pack(side = 'top', fill = 'both', expand = True)
        
        #!top frame
        self.topFrame = tk.Frame(self.window)
        self.topFrame.pack(fill='x')

        #!app name in left corner of topframe
        self.logo = tk.Label(self.topFrame, text = 'Schedular > Admin Dashboard > Manage Timetables', font=LargeFont)
        self.logo.pack(padx=20, pady=10, side='left')

        #!logout button at top right corner of topframe, redirects userback to startpage
        self.backBtn = tk.Button(self.topFrame, text = 'Back to Dashboard', font=LargeFont, 
        command=lambda:self.back())
        self.backBtn.pack(padx=(5,20), pady=10, side='right')
        
        #!main frame, where the main componets of the management system reside
        self.mainFrame = tk.Frame(self.window, bg = '#2c2f33')
        self.mainFrame.pack(padx = 20, pady = 10, fill = 'both', expand = True)
        
        #!creating the timetable database viewing treeview widget
        self.createTimetableDBViewer()
        self.createDataFrame()
        self.createControlsFrame()

#!########################################################################
#!function that creates a database style treeview widget to view the timetable records
    def createTimetableDBViewer(self):
        #!setting the style of the treeview widget 
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Treeview', background = '#2c2f33', foreground = '#7289da', rowheight = 25, fieldbackground = '#2c2f33')
        #!setting the colour of the record when its selected
        style.map('Treview', background=[('selected', '#23272a')])

        #!timetable database widget frame
        self.dbWidget = tk.Frame(self.mainFrame, background = '#2c2f33')
        self.dbWidget.grid(row=3, column=0, padx = 20, pady = 10, sticky='ew')

        #!scrollbar on right side of the sdbwidget
        self.tree_scroll = tk.Scrollbar(self.dbWidget)
        self.tree_scroll.pack(side=RIGHT, fill='y')

        #!treeview widget, setting the scorll command to the scroll of the scrollbar
        self.dbViewer = ttk.Treeview(self.dbWidget, yscrollcommand=self.tree_scroll.set, selectmode='extended')
        self.dbViewer.pack(fill='x')

        #!configuring the scrollbar to view/scroll in the y axies of the sdbviewer
        self.tree_scroll.config(command=self.dbViewer.yview)

        #!setting the column titles to the fields in the timetable database
        self.dbViewer['columns'] = ['Class ID', 'Classroom', 'Subject', 'Teacher', 'Day', 'Period']
        
        #!configuring the first 'ghost' column to be width 0, so basically invisible
        self.dbViewer.column('#0', width=0, stretch=NO)
        self.dbViewer.heading('#0', text = '', anchor = CENTER)

        #!for each columns title, setting the treeview columns, and configuring them to look better
        for i in self.dbViewer['columns']:
            self.dbViewer.column(i, anchor = CENTER, width = 100, minwidth = 25)
            self.dbViewer.heading(i, text = i, anchor = CENTER)

        #!binding a click and release of a mouse button while on a record, to run the selectdata function
        self.dbViewer.bind('<ButtonRelease-1>', self.selectData)

#!########################################################################
    def createDataFrame(self):
        #!data frame is where the widgets of the databases form reside
        self.data_frame = tk.LabelFrame(self.mainFrame, text='Record', background = '#2c2f33')
        self.data_frame.grid(row=4, column=0, padx = 20, pady = 10, sticky='ew')
        
        #!classId(integer) entry for the student record
        self.idLabel = tk.Label(self.data_frame, text = 'Class ID : ', bg = '#2c2f33')
        self.idLabel.grid(row = 2, column = 0, padx=20, pady=(10,0), sticky='w')
        self.idEntry = tk.Entry(self.data_frame, width = 20, font = ('Verdana', 15), fg='grey')
        self.setIDEntryTo(value='ID Is Auto Assigned')
        self.idEntry.grid(row = 3, column = 0, padx=20, pady=5, sticky='w')

        #!classroom(string) entry
        self.classroomLabel = tk.Label(self.data_frame, text = 'Classroom : ', bg = '#2c2f33')
        self.classroomLabel.grid(row = 2, column = 1, padx=20, pady=(10,0), sticky='w')
        self.classroomEntry = tk.Entry(self.data_frame, width = 20, font = ('Verdana', 15)) 
        self.classroomEntry.grid(row = 3, column = 1, padx=20, pady=5, sticky='w')
        
        #!subject(string) entry
        self.subjectLabel = tk.Label(self.data_frame, text = 'Subject : ', bg = '#2c2f33')
        self.subjectLabel.grid(row = 2, column = 2, padx=20, pady=(10,0), sticky='w')
        self.subjectEntry = tk.Entry(self.data_frame, width = 20, font = ('Verdana', 15)) 
        self.subjectEntry.grid(row = 3, column = 2, padx=20, pady=5, sticky='w')

        #!teachername(string) entry
        self.teacherNameLabel = tk.Label(self.data_frame, text = 'Teacher : ', bg = '#2c2f33')
        self.teacherNameLabel.grid(row = 4, column = 0, padx=20, pady=(10,0), sticky='w')
        self.teacherNameEntry = tk.Entry(self.data_frame, width = 20, font = ('Verdana', 15)) 
        self.teacherNameEntry.grid(row = 5, column = 0, padx=20, pady=(5,10), sticky='w')

        #!day(int) entry
        self.dayLabel = tk.Label(self.data_frame, text = 'Day : ', bg = '#2c2f33')
        self.dayLabel.grid(row = 4, column = 1, padx=20, pady=(10,0), sticky='w')
        self.dayEntry = tk.Entry(self.data_frame, width = 20, font = ('Verdana', 15)) 
        self.dayEntry.grid(row = 5, column = 1, padx=20, pady=(5,10), sticky='w')

        #!period(int) entry
        self.periodLabel = tk.Label(self.data_frame, text = 'Period : ', bg = '#2c2f33')
        self.periodLabel.grid(row = 4, column = 2, padx=20, pady=(10,0), sticky='w')
        self.periodEntry = tk.Entry(self.data_frame, width = 20, font = ('Verdana', 15)) 
        self.periodEntry.grid(row = 5, column = 2, padx=20, pady=(5,10), sticky='w')

#!########################################################################
    def createControlsFrame(self):
        #!commands frame is where the buttons that initiate managemnt functions reside
        self.commands_frame = tk.LabelFrame(self.mainFrame, text='Commands', background = '#2c2f33')
        self.commands_frame.grid(row=5, column=0, padx = 20, pady = 10, sticky='ew')

        #!show button, when clicked runs the showdata function, shows database records on the treeview widget
        self.showBtn = tk.Button(self.commands_frame, text = 'Show Info', width=14,
        command = lambda: self.showData())
        self.showBtn.grid(row= 1, column=0, padx = 20, pady = 10, sticky='w')

        #!add button, when clicked runs the adddata function, adds inputed data as a new record to the db
        self.addBtn = tk.Button(self.commands_frame, text = 'Add Record', width=14, 
        command = lambda: self.addData())
        self.addBtn.grid(row= 1, column=1, padx = 20, pady = 10, sticky='w')

        #!update button, when clicked runs the update function, updates a record in the db using the new inputed data
        self.updateBtn = tk.Button(self.commands_frame, text = 'Update Record', width=14, 
        command = lambda: self.updateData())
        self.updateBtn.grid(row= 1, column=2, padx = 20, pady = 10, sticky='w')

        #!delete button, when clicked runs the deletedata function, deletes the record that is selected on the treeview
        self.deleteBtn = tk.Button(self.commands_frame, text = 'Delete Record', width=14, 
        command = lambda: self.deleteData())
        self.deleteBtn.grid(row= 1, column=3, padx = 20, pady = 10, sticky='w')

        #!select button, runs the selectdata function, selects the record highlighted and autofills the inputs with that records data
        self.selectBtn = tk.Button(self.commands_frame, text = 'Select Record', width=14, 
        command = lambda: self.selectData(''))
        self.selectBtn.grid(row= 1, column=4, padx = 20, pady = 10, sticky='w')
        
        #!clear button, runs the clearentries function, clears all the entry widgets in the form
        self.clearBtn = tk.Button(self.commands_frame, text = 'Clear Entry Boxes', width=14, 
        command = lambda: self.clearEntries())
        self.clearBtn.grid(row= 1, column=5, padx = 20, pady = 10, sticky='w')

        #!warning label informs the Admin what they have changed or done wrong
        self.warningLbl = tk.Label(self.mainFrame, text='No Changes.', bg='#2c2f33')
        self.warningLbl.grid(row=6, column=0, columnspan=5, padx = 20, pady = 10, sticky='w')

#!########################################################################
    #!redirects user back to admin dashboard page,
    #!clears all activities carried out by Admin, to keep privacy of data
    #!wipes out any data in the sdbviewer and form inputs, sets warning message back to default
    def back(self):
       self.controller.show_frame(AdminDashboard.Page)
       self.clearEntries()
       self.clearCells()
       self.warningLbl.config(text='No Changes.')

#!########################################################################
    #!shows records of the student database on the sdbviewer
    def showData(self):
        self.clearEntries()
        self.createTimetableDBViewer()
        cur.execute('SELECT * FROM Class')
        for row in (cur.fetchall()):
            self.dbViewer.insert(parent='', index='end', values=(row[0],row[1],row[2],row[3],row[4],row[5]))
        self.warningLbl.config(text='Class Records Displayed.', fg='#7289da')

    #!adds data entered into the form to the student database as a new record
    def addData(self):
        values = ['','','','','']
        lessonExists = self.checkIfUserExists(self.dayEntry.get(), self.periodEntry.get(), values)

        if lessonExists == False:
            if self.classroomEntry.get() != '' and self.subjectEntry.get() != '' and self.teacherNameEntry.get() != '' and self.dayEntry.get() != ''and self.periodEntry.get() != '':
                if self.dayEntry.get().isdigit() and self.periodEntry.get().isdigit():
                    newData = (self.classroomEntry.get(), self.subjectEntry.get(), self.teacherNameEntry.get(), self.dayEntry.get(), self.periodEntry.get())
                    cur.execute('INSERT INTO Class(ClassroomID,SubjectName,TeacherName,Day,Period) VALUES(?,?,?,?,?)', newData)
                    self.showData()
                    self.warningLbl.config(text='New Record Added.', fg='#7289da')
                else:
                    self.warningLbl.config(text='Day And Period Entry Must Be Integers!', fg='red')
            else:
                self.warningLbl.config(text='Not All Fields Are Filled!', fg='red')
        else:
            self.warningLbl.config(text='Lesson Already Exists', fg='red')

    #!updates records based on the inputs into the form for that record
    def updateData(self):
        selected = self.dbViewer.focus()
        values = self.dbViewer.item(selected, 'values')
        lessonExists = self.checkIfUserExists(self.dayEntry.get(), self.periodEntry.get(), values)

        if lessonExists == False:
            if selected != '':
                if self.classroomEntry.get() != '' and self.subjectEntry.get() != '' and self.teacherNameEntry.get() != '' and self.dayEntry.get() != ''and self.periodEntry.get() != '':
                    if self.dayEntry.get().isdigit() and self.periodEntry.get().isdigit():
                        cur.execute('''
                                    UPDATE Class 
                                    SET ClassroomId=?, SubjectName=?, TeacherName=?, Day=?, Period=?
                                    WHERE ClassID=?
                                    ''', 
                                    self.classroomEntry.get(), 
                                    self.subjectEntry.get(),
                                    self.teacherNameEntry.get(),
                                    self.dayEntry.get(),
                                    self.periodEntry.get(),
                                    values[0]
                        )
                        cur.commit()
                        self.showData()
                        self.warningLbl.config(text='Record Updated.', fg='#7289da')
                    else:
                        self.warningLbl.config(text='Day And Period Entry Must Be Integers!', fg='red')
                else:
                    self.warningLbl.config(text='Not All Fields Are Filled!', fg='red')
            else:
                self.warningLbl.config(text='No Record Selected!', fg='red')
        else:
            self.warningLbl.config(text='Lesson Already Exists', fg='red')

    #!deletes the record selected from the sdbviewer and the database itself
    def deleteData(self):
        selected = self.dbViewer.focus()
        values = self.dbViewer.item(selected, 'values')

        if selected != '':
            cur.execute('DELETE FROM Class WHERE ClassID=?', values[0])
            cur.commit()
            self.showData()
            self.warningLbl.config(text='Record Deleted.', fg='#7289da')
        else:
            self.warningLbl.config(text='No Record Selected!', fg='red')
            
    #!selects record and autofills the form with that record data
    def selectData(self, event):
        self.clearEntries()
        selected = self.dbViewer.focus()
        values = self.dbViewer.item(selected, 'values')
        if selected != '':
            self.setIDEntryTo(value=values[0])
            self.classroomEntry.insert(0, values[1])
            self.subjectEntry.insert(0, values[2])
            self.teacherNameEntry.insert(0, values[3])
            self.dayEntry.insert(0, values[4])
            self.periodEntry.insert(0, values[5])
            self.warningLbl.config(text='Class Record Selected.', fg='#7289da')

    #!clears all the entries in the form
    def clearEntries(self):
        self.setIDEntryTo(value='ID Is Auto Assigned')
        self.idEntry.delete(0, 'end')
        self.classroomEntry.delete(0, 'end')
        self.subjectEntry.delete(0, 'end')
        self.teacherNameEntry.delete(0, 'end')
        self.dayEntry.delete(0, 'end')
        self.periodEntry.delete(0, 'end')

    #!clears all the cells in the dbviewer
    def clearCells(self):
        self.dbViewer.delete(*self.dbViewer.get_children())

    #!sets the text of the id entry to default or a specified value
    def setIDEntryTo(self, value):
        self.idEntry.config(state='normal', cursor='left_ptr')
        self.idEntry.delete(0,'end')
        self.idEntry.insert(0, value)
        self.idEntry.config(state='readonly')

    #!checks if the new user data inputed already exists
    def checkIfUserExists(self, day, period, values):
        cur.execute('SELECT * FROM Class')
        for row in (cur.fetchall()):
            if row[4] == day and row[5] == period:
                lessonExists = True
                if row[4]==day==values[4] and row[5]==period==values[5]:
                    lessonExists = False
                    break
                else:
                    lessonExists = True
                    break
            else:
                lessonExists = False

        return lessonExists