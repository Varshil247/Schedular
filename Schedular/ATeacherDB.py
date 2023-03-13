import tkinter as tk
from tkinter import ttk
from tkinter.constants import CENTER, NO, RIGHT
from hashlib import *

from MDBConnection import *
import AdminDashboard

#!########################################################################
LargeFont = ('Verdana', 12)

#!class of a page which runs the teacher databse management system
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
        self.logo = tk.Label(self.topFrame, text = 'Schedular > Admin Dashboard > Manage Teachers', font=LargeFont)
        self.logo.pack(padx=20, pady=10, side='left')

        #!logout button at top right corner of topframe, redirects userback to startpage
        self.backBtn = tk.Button(self.topFrame, text = 'Back to Dashboard', font=LargeFont, 
        command=lambda:self.back())
        self.backBtn.pack(padx=(5,20), pady=10, side='right')

        #!main frame, where the main componets of the management system reside
        self.mainFrame = tk.Frame(self.window, bg = '#2c2f33')
        self.mainFrame.pack(padx = 20, pady = 10, fill = 'both', expand = True)
        
        #!creating the teacher database viewing treeview widget
        self.createTeacherDBViewer()
        self.createDataFrame()
        self.createCommandsFrame()

#!########################################################################
#!function that creates a database style treeview widget to view the teacher records
    def createTeacherDBViewer(self):
        #!setting the style of the treeview widget 
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Treeview', background = '#2c2f33', foreground = '#7289da', rowheight = 25, fieldbackground = '#2c2f33')
        #!setting the colour of the record when its selected
        style.map('Treview', background=[('selected', '#23272a')])

        #!teacher database widget frame
        self.dbWidget = tk.Frame(self.mainFrame, background = '#2c2f33')
        self.dbWidget.grid(row=2, column=0, padx = 20, pady = 10, sticky='ew')

        #!scrollbar on right side of the sdbwidget
        self.tree_scroll = tk.Scrollbar(self.dbWidget)
        self.tree_scroll.pack(side=RIGHT, fill='y')

        #!treeview widget, setting the scorll command to the scroll of the scrollbar
        self.dbViewer = ttk.Treeview(self.dbWidget, yscrollcommand=self.tree_scroll.set, selectmode='extended')
        self.dbViewer.pack(fill='x')
        
        #!configuring the scrollbar to view/scroll in the y axies of the sdbviewer
        self.tree_scroll.config(command=self.dbViewer.yview)

        #!setting the column titles to the fields in the teacher database
        self.dbViewer['columns'] = ['Teacher ID','Username','Password','Firstname','Surname','Subject']
        
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
        self.data_frame = tk.LabelFrame(self.mainFrame, text='Record', bg = '#2c2f33')
        self.data_frame.grid(row=3, column=0, padx = 20, pady = 10, sticky='ew')

        #!id(integer) entry for the teacher record
        self.idLabel = tk.Label(self.data_frame, text = 'ID : ', bg = '#2c2f33')
        self.idLabel.grid(row = 2, column = 0, padx=20, pady=(10,0), sticky='w')
        self.idEntry = tk.Entry(self.data_frame, width = 20, font = ('Verdana', 15), fg='grey')
        self.setIDEntryTo(value='ID Is Auto Assigned')
        self.idEntry.grid(row = 3, column = 0, padx=20, pady=5, sticky='w')

        #!usernmame(string) entry
        self.usernameLabel = tk.Label(self.data_frame, text = 'Username : ', bg = '#2c2f33')
        self.usernameLabel.grid(row = 2, column = 1, padx=20, pady=(10,0), sticky='w')
        self.usernameEntry = tk.Entry(self.data_frame, width = 20, font = ('Verdana', 15)) 
        self.usernameEntry.grid(row = 3, column = 1, padx=20, pady=5, sticky='w')

        #!password(string) entry
        self.passwordLabel = tk.Label(self.data_frame, text = 'Password : ', bg = '#2c2f33')
        self.passwordLabel.grid(row = 2, column = 2, padx=20, pady=(10,0), sticky='w')
        self.passwordEntry = tk.Entry(self.data_frame, width = 20, font = ('Verdana', 15)) 
        self.passwordEntry.grid(row = 3, column = 2, padx=20, pady=5, sticky='w')

        #!firstname(string) entry
        self.firstnameLabel = tk.Label(self.data_frame, text = 'Firstname : ', bg = '#2c2f33')
        self.firstnameLabel.grid(row = 4, column = 0, padx=20, pady=(10,0), sticky='w')
        self.firstnameEntry = tk.Entry(self.data_frame, width = 20, font = ('Verdana', 15)) 
        self.firstnameEntry.grid(row = 5, column = 0, padx=20, pady=(5,10), sticky='w')

        #!surname(string) entry
        self.surnameLabel = tk.Label(self.data_frame, text = 'Surname : ', bg = '#2c2f33')
        self.surnameLabel.grid(row = 4, column = 1, padx=20, pady=(10,0), sticky='w')
        self.surnameEntry = tk.Entry(self.data_frame, width = 20, font = ('Verdana', 15)) 
        self.surnameEntry.grid(row = 5, column = 1, padx=20, pady=(5,10), sticky='w')

        #!subject(string) entry
        self.subjectLabel = tk.Label(self.data_frame, text = 'Subject : ', bg = '#2c2f33')
        self.subjectLabel.grid(row = 4, column = 2, padx=20, pady=(10,0), sticky='w')
        self.subjectEntry = tk.Entry(self.data_frame, width = 20, font = ('Verdana', 15)) 
        self.subjectEntry.grid(row = 5, column = 2, padx=20, pady=(5,10), sticky='w')

#!########################################################################
    def createCommandsFrame(self):
        #!commands frame is where the buttons that initiate managemnt functions reside
        self.commands_frame = tk.LabelFrame(self.mainFrame, text='Commands', background = '#2c2f33')
        self.commands_frame.grid(row=4, column=0, padx = 20, pady = 10, sticky='ew')

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
        self.warningLbl.grid(row=5, column=0, padx = 20, pady = 10, sticky='w')

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
    #!shows records of the teacher database on the sdbviewer
    def showData(self):
        self.clearEntries()
        self.createTeacherDBViewer()
        cur.execute('SELECT * FROM Teacher')
        for row in (cur.fetchall()):
            self.dbViewer.insert(parent='', index='end', values=(row[0],row[1],row[2],row[3],row[4],row[5]))
        self.warningLbl.config(text='Teacher Records Displayed.', fg='#7289da')

    #!adds data entered into the form to the teacher database as a new record
    def addData(self):
        values = ['','','','','','']
        userExists = self.checkIfUserExists(self.usernameEntry.get(), values)

        if userExists == False:
            encryptedPassword = sha256(bytes(self.passwordEntry.get(), encoding = 'utf-8')).hexdigest()
            if self.usernameEntry.get() != '' and self.passwordEntry.get() != '' and self.firstnameEntry.get() != '' and self.surnameEntry.get() != '' and self.subjectEntry.get() != '':
                newData = (self.usernameEntry.get(), encryptedPassword, self.firstnameEntry.get(), self.surnameEntry.get(), self.subjectEntry.get())
                cur.execute('INSERT INTO Teacher(Username,Password,Firstname,Surname,Subject) VALUES(?,?,?,?,?)', newData)
                self.showData()
                self.warningLbl.config(text='New Record Added.', fg='#7289da')
            else:
                self.warningLbl.config(text='Not All Fields Are Filled!', fg='red')
        else:
            self.warningLbl.config(text='User Already Exists', fg='red')

    #!updates records based on the inputs into the form for that record
    def updateData(self):
        selected = self.dbViewer.focus()
        values = self.dbViewer.item(selected, 'values')
        userExists = self.checkIfUserExists(self.usernameEntry.get(), values)

        if userExists == False:
            if selected != '':
                if self.usernameEntry.get() != '' and self.passwordEntry.get() != '' and self.firstnameEntry.get() != '' and self.surnameEntry.get() != '' and self.subjectEntry.get() != '':
                    cur.execute('''
                                UPDATE Teacher 
                                SET Firstname=?, Surname=?, Subject=? 
                                WHERE TeacherID=?
                                ''', 
                                self.firstnameEntry.get(), 
                                self.surnameEntry.get(), 
                                self.subjectEntry.get(), 
                                values[0]
                    )
                    cur.commit()
                    self.showData()
                    self.warningLbl.config(text='Record Updated.', fg='#7289da')
                else:
                    self.warningLbl.config(text='Not All Fields Are Filled!', fg='red')
            else:
                self.warningLbl.config(text='No Record Selected!', fg='red')
        else:
            self.warningLbl.config(text='User Already Exists', fg='red')

    #!deletes the record selected from the sdbviewer and the database itself
    def deleteData(self):
        selected = self.dbViewer.focus()
        values = self.dbViewer.item(selected, 'values')

        if selected != '':
            cur.execute('DELETE FROM Teacher WHERE TeacherID=?', values[0])
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
            self.idEntry.insert(0, values[0])
            self.usernameEntry.insert(0, values[1])
            self.passwordEntry.insert(0, values[2])
            self.firstnameEntry.insert(0, values[3])
            self.surnameEntry.insert(0, values[4])
            self.subjectEntry.insert(0, values[5])
            self.warningLbl.config(text='Teacher Record Selected.', fg='#7289da')

    #!clears all the entries in the form
    def clearEntries(self):
        self.idEntry.delete(0, 'end')
        self.usernameEntry.delete(0, 'end')
        self.passwordEntry.delete(0, 'end')
        self.firstnameEntry.delete(0, 'end')
        self.surnameEntry.delete(0, 'end')
        self.subjectEntry.delete(0, 'end')

    #!clears all the cells in the dbviewerteacher
    def clearCells(self):
        self.dbViewer.delete(*self.dbViewer.get_children())

    #!sets the text of the id entry to default or a specified value
    def setIDEntryTo(self, value):
        self.idEntry.config(state='normal', cursor='left_ptr')
        self.idEntry.delete(0,'end')
        self.idEntry.insert(0, value)
        self.idEntry.config(state='readonly')

    #!checks if the new user data inputed already exists
    def checkIfUserExists(self, username, values):
        cur.execute('SELECT * FROM Teacher')
        for row in (cur.fetchall()):
            if row[1]==username:
                userExists = True
                if row[1]==username and username==values[1]:
                    userExists = False
                    break
                else:
                    userExists = True
                    break
            else:
                userExists = False

        return userExists
