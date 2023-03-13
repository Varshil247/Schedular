import tkinter as tk
from tkinter import ttk
from hashlib import *
import datetime

from MDBConnection import *
import MData
import AdminDashboard, TeacherDashboard, StudentDashboard

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

        self.logo = tk.Label(self.topFrame, text = 'Schedular', font=LargeFont)
        self.logo.pack(padx=5, pady=10, side='left')

        self.signupBtn = tk.Button(self.topFrame, text = 'Signup', background='#23272a', activebackground='#23272a', fg='#7289da', font=LargeFont, 
        command=lambda:[self.delFrames(), self.signupsys()])
        self.signupBtn.pack(padx=(5,20), pady=10, side='right')

        self.loginBtn = tk.Button(self.topFrame, text = 'Login', background='#23272a', activebackground='#23272a', fg='#7289da', font=LargeFont, 
        command=lambda:[self.delFrames(), self.loginsys()])
        self.loginBtn.pack(padx=(20,5), pady=10, side='right')

        self.authSysFrame = tk.Frame(self.window, bg = '#2c2f33')
        self.authSysFrame.pack(padx=20, pady=20)

        self.delFrames()
        self.loginsys()

        #return('authSys page initialized')
#!########################################################################
#! Login system
    def loginsys(self):
        self.loginLbl = tk.Label(self.authSysFrame, text = 'Login', bg = '#2c2f33', font=LargeFont, width=30)
        self.loginLbl.grid(row = 1, column = 1, padx = 20, pady = 10)
        
        self.usernameLbl = tk.Label(self.authSysFrame, text = 'Username', bg = '#2c2f33')
        self.usernameLbl.grid(row = 2, column = 1, padx = 20, sticky = 'w')
        self.login_usernameInput = tk.Entry(self.authSysFrame, width = 20, font = LargeFont)
        self.login_usernameInput.grid(row = 3, column = 1, padx = 20, pady = 10, sticky = 'ew')
        self.login_usernameInput.focus()

        self.passwordFrame = tk.Frame(self.authSysFrame, bg = '#2c2f33')
        self.passwordFrame.grid(row = 4, column = 1, padx = 20, sticky = 'w')
        self.passwordLbl = tk.Label(self.passwordFrame, text = 'Password', bg = '#2c2f33')
        self.passwordLbl.grid(row = 1, column = 1, sticky = 'w')
        self.login_passwordInput = tk.Entry(self.passwordFrame, width = 26, show = '•', font = LargeFont)
        self.login_passwordInput.grid(row = 2, column = 1, padx = 0, pady = 10, sticky = 'ew')
        
        toggleText = 'Un-hide'
        self.unhideToggle = tk.Button(self.passwordFrame, text = toggleText, width=6,
        command=lambda:self.unhideToggleFunc(entryBox=self.login_passwordInput, toggle=self.unhideToggle, toggleText=toggleText))
        self.unhideToggle.grid(row=2, column=2, padx = 0, pady = 10, sticky = 'ew') 

        userTypes = ['Admin','Teacher','Student']
        self.userTypeLbl = tk.Label(self.authSysFrame, text = 'User Type', bg = '#2c2f33')
        self.userTypeLbl.grid(row = 5, column = 1, padx = 20, sticky = 'w')
        self.userTypeEntry = ttk.Combobox(self.authSysFrame, value = userTypes, state='readonly', width = 20, font = LargeFont) 
        self.userTypeEntry.current(0)
        self.userTypeEntry.grid(row = 6, column = 1, padx=20, pady=10, sticky = 'ew')
        
        self.login_submitBtn = tk.Button(self.authSysFrame, text = 'Continue', width=30,
        command = lambda: self.login())
        self.login_submitBtn.grid(row = 7, column = 1, padx = 20, pady = 10, sticky = 'ew')
        
        self.signupBtn = tk.Button(self.authSysFrame, text = '''Don't have an account? Sign up here.''', width=30,
        command = lambda: [self.delFrames(), self.signupsys()])
        self.signupBtn.grid(row = 8, column = 1, padx = 20, pady = (10,20), sticky = 'ew')

        self.loginWarningLbl = tk.Label(self.authSysFrame, text = '', bg = '#2c2f33')

        return('User Is Using The Login System')

#!########################################################################
#!login backend
    def login(self):
        loginSuccessful = False

        username = self.login_usernameInput.get()
        password = self.login_passwordInput.get()
        userType = self.userTypeEntry.get()
        encryptedPassword = sha256(bytes(password, encoding = 'utf-8')).hexdigest()
        lastLoggedIn = '{:%d/%m/%Y %H:%M:%S}'. format(datetime.datetime.now())
        
        self.loginWarningLbl.destroy()
        self.loginWarningLbl = tk.Label(self.authSysFrame, text = '', bg = '#2c2f33')
        self.loginWarningLbl.grid(row = 9, column = 1, padx = 10, pady = 10)

        inputLabels = [self.usernameLbl, self.passwordLbl]
        self.setLabelsToDefault(labels=inputLabels)
        if username == '' or password == '':
            self.loginWarningLbl.config(text='Enter Credentials !', fg='red')
            if username == '':
                self.usernameLbl.config(text='Username', fg='red')
            if password == '':
                self.passwordLbl.config(text='Password', fg='red')
        
        else:
            try:
                db_data = []
                if userType == 'Admin':
                    cur.execute('''SELECT * FROM Admin''')
                if userType == 'Teacher':
                    cur.execute('''SELECT * FROM Teacher''')
                if userType == 'Student':
                    cur.execute('''SELECT * FROM Student''')

                for record in cur.fetchall():
                    db_data.append(record)

                for userInfo in db_data:
                    if userInfo[1] == username and userInfo[2] == encryptedPassword:
                        MData.username = username
                        MData.userType = userType
                        print(MData.username, MData.userType, 'Logged In')
                        self.usernameLbl.config(text='Username', fg='#7289da')
                        self.passwordLbl.config(text='Password', fg='#7289da')
                        self.loginWarningLbl.config(text='Successful Login.', fg='#7289da')

                        if userType == 'Admin':
                            cur.execute('''UPDATE Admin
                                        SET lastLoggedIn = ? 
                                        WHERE password = ?''',
                                        lastLoggedIn, encryptedPassword)
                            conn.commit()
                            self.controller.show_frame(AdminDashboard.Page)

                        if userType == 'Teacher':
                            cur.execute('''UPDATE Teacher
                                        SET lastLoggedIn = ?
                                        WHERE password = ?''',
                                        lastLoggedIn, encryptedPassword)
                            conn.commit()
                            self.controller.show_frame(TeacherDashboard.Page)

                        if userType == 'Student':
                            cur.execute('''UPDATE Student 
                                        SET lastLoggedIn = ? 
                                        WHERE password = ?''', 
                                        lastLoggedIn, encryptedPassword)
                            conn.commit()
                            self.controller.show_frame(StudentDashboard.Page)

                        self.delFrames()
                        self.loginsys()

                        loginSuccessful = True
                        break

                    else:
                        self.setLabelsToDefault(labels=inputLabels)
                        self.loginWarningLbl.config(text='Wrong Credentials !', fg='red')

                        if userInfo[1] != username:
                            self.usernameLbl.config(text='Username', fg='red')
                        if userInfo[2] != encryptedPassword:
                            self.passwordLbl.config(text='Password', fg='red')
                        
                        loginSuccessful = False

            except pyodbc.Error as e: 
                print('Error in Connection', e)
                loginSuccessful = False

        return(loginSuccessful)

#!########################################################################
#! Signup system
    def signupsys(self):
        self.signupLbl = tk.Label(self.authSysFrame, text = 'Signup', bg = '#2c2f33', font=LargeFont, width=30)
        self.signupLbl.grid(row = 1, column = 1, padx = 20, pady = 10)

        self.usernameLbl = tk.Label(self.authSysFrame, text = 'Username', bg = '#2c2f33')
        self.usernameLbl.grid(row = 2, column = 1, padx = 20, sticky = 'w')
        self.signup_usernameInput = tk.Entry(self.authSysFrame, width = 20, font = LargeFont)
        self.signup_usernameInput.grid(row = 3, column = 1, padx = 20, pady = 10, sticky = 'ew')
        self.signup_usernameInput.focus()

        self.passwordFrame = tk.Frame(self.authSysFrame, bg = '#2c2f33')
        self.passwordFrame.grid(row = 4, column = 1, padx = 20, sticky = 'w')
        self.passwordLbl = tk.Label(self.passwordFrame, text = 'Password', bg = '#2c2f33')
        self.passwordLbl.grid(row = 1, column = 1, sticky = 'w')
        self.signup_passwordInput = tk.Entry(self.passwordFrame, width = 26, show = '•', font = LargeFont)
        self.signup_passwordInput.grid(row = 2, column = 1, pady = (10,2), sticky = 'ew')

        toggleText = 'Un-hide'
        self.unhideToggle = tk.Button(self.passwordFrame, text = toggleText, width=6,
        command=lambda:self.unhideToggleFunc(entryBox=self.signup_passwordInput, toggle=self.unhideToggle, toggleText=toggleText))
        self.unhideToggle.grid(row=2, column=2, padx = 0, pady = (10,2), sticky = 'ew') 
        self.passwordInfo = tk.Label(self.passwordFrame, text='Password must have atleast: 8 characters, 1 uppercase, 1 special character, 1 number.', font=('halvetica', 8), bg = '#2c2f33', fg='grey')
        self.passwordInfo.grid(row=3, column=1, padx=0, pady=0, sticky='w')

        self.password2Frame = tk.Frame(self.authSysFrame, bg = '#2c2f33')
        self.password2Frame.grid(row = 5, column = 1, padx = 20, sticky = 'w')
        self.password2Lbl = tk.Label(self.password2Frame, text = 'Confirm Password', bg = '#2c2f33')
        self.password2Lbl.grid(row = 1, column = 1, sticky = 'w')
        self.signup_password2Input = tk.Entry(self.password2Frame, width = 26, show = '•', font = LargeFont)
        self.signup_password2Input.grid(row = 2, column = 1, pady = (10,2), sticky = 'ew')
        
        toggle2Text = 'Un-hide'
        self.unhide2Toggle = tk.Button(self.password2Frame, text = toggle2Text, width=6,
        command=lambda:self.unhideToggleFunc(entryBox=self.signup_password2Input, toggle=self.unhide2Toggle, toggleText=toggle2Text))
        self.unhide2Toggle.grid(row=2, column=2, padx = 0, pady = (10,2), sticky = 'ew') 
        self.passwordInfo = tk.Label(self.password2Frame, text='Password must have atleast: 8 characters, 1 uppercase, 1 special character, 1 number.', font=('halvetica', 8), bg = '#2c2f33', fg='grey')
        self.passwordInfo.grid(row=3, column=1, padx=0, pady=0, sticky='w')

        self.fnameLbl = tk.Label(self.authSysFrame, text = 'First Name', bg = '#2c2f33')
        self.fnameLbl.grid(row = 6, column = 1, padx = 20, sticky = 'w')
        self.signup_firstnameInput = tk.Entry(self.authSysFrame, width = 20, font = LargeFont)
        self.signup_firstnameInput.grid(row = 7, column = 1, padx = 20, pady = 10, sticky = 'ew')

        self.snameLbl = tk.Label(self.authSysFrame, text = 'Surname', bg = '#2c2f33')
        self.snameLbl.grid(row = 8, column = 1, padx = 20, sticky = 'w')
        self.signup_surnameInput = tk.Entry(self.authSysFrame, width = 20, font = LargeFont)
        self.signup_surnameInput.grid(row = 9, column = 1, padx = 20, pady = 10, sticky = 'ew')
        
        usertypes = ['Admin','Teacher','Student']
        self.userTypeLbl = tk.Label(self.authSysFrame, text = 'User Type', bg = '#2c2f33')
        self.userTypeLbl.grid(row = 10, column = 1, padx = 20, sticky = 'w')
        self.userTypeEntry = ttk.Combobox(self.authSysFrame, value = usertypes, state='readonly', width = 20, font = LargeFont) 
        self.userTypeEntry.current(0)
        self.userTypeEntry.grid(row = 11, column = 1, padx=20, pady=10, sticky='ew')

        self.signup_submitButton = tk.Button(self.authSysFrame, text = 'Continue', width=30,
        command = lambda: self.signup())
        self.signup_submitButton.grid(row = 12, column = 1, padx = 20, pady = 10, sticky = 'ew')
        
        self.loginBtn = tk.Button(self.authSysFrame, text = '''Already have an account? Login here.''', width=30,
        command = lambda: [self.delFrames(), self.loginsys()])
        self.loginBtn.grid(row = 13, column = 1, padx = 20, pady = (10,20), sticky = 'ew')

        self.signupWarningLbl = tk.Label(self.authSysFrame, text = '')

        return('User Is Using The Signup System')

#!########################################################################
#!signup backend
    def signup(self):
        userExists = False
        signupSuccessful = False

        username = self.signup_usernameInput.get()
        password = self.signup_passwordInput.get()
        password2 = self.signup_password2Input.get()
        firstname = self.signup_firstnameInput.get()
        surname = self.signup_surnameInput.get()
        userType = self.userTypeEntry.get()
        encryptedPassword = sha256(bytes(password, encoding = 'utf-8')).hexdigest()
        signedUp = '{:%d/%m/%Y %H:%M:%S}'. format(datetime.datetime.now())

        self.signupWarningLbl.destroy()
        self.signupWarningLbl = tk.Label(self.authSysFrame, text = '', bg = '#2c2f33')
        self.signupWarningLbl.grid(row = 14, column = 1, padx = 10, pady = 10)

        inputLabels = [self.usernameLbl, self.passwordLbl, self.password2Lbl, self.fnameLbl, self.snameLbl]
        self.setLabelsToDefault(labels=inputLabels)
        if username == '' or password == '' or password2 == '' or firstname == '' or surname == '':
            self.signupWarningLbl.config(text='Enter Information !', fg='red')
            if username == '':
                self.usernameLbl.config(text='Username', fg='red')
            if password == '':
                self.passwordLbl.config(text='Password', fg='red')
            if password2 == '':
                self.password2Lbl.config(text='Confirm Password', fg='red')
            if firstname == '':
                self.fnameLbl.config(text='First Name', fg='red')
            if surname == '':
                self.snameLbl.config(text='Surname', fg='red')

        passwordValid = True
        passwordImprovement = ''
        isUpper = any(char.isupper() for char in password)
        isSpecial = any(not char.isalnum() for char in password)
        isNumeric = any(char.isdigit() for char in password)

        if len(password) < 8:
            passwordImprovement += ' 8 Characters,'
            passwordValid = False
        if isUpper != True:
            passwordImprovement += ' 1 Uppercase,'
            passwordValid = False
        if isSpecial != True:
            passwordImprovement += ' 1 Special Character,'
            passwordValid = False
        if isNumeric != True:
            passwordImprovement += ' 1 Number'
            passwordValid = False

        if username != '' or password != '' or password2 != '' or firstname != '' or surname != '':
            if passwordValid == True:
                if password == password2:
                    try:
                        db_data = []
                        if userType == 'Admin':
                            cur.execute('''SELECT * FROM Admin''')
                        if userType == 'Teacher':
                            cur.execute('''SELECT * FROM Teacher''')
                        if userType == 'Student':
                            cur.execute('''SELECT * FROM Student''')

                        for row in cur.fetchall():
                            db_data.append(row)
                        
                        for usersInfo in db_data:
                            if usersInfo[1] == username:
                                self.signupWarningLbl.config(text='User Already Exists!', fg='red')
                                signupSuccessful = False
                                userExists = True 

                    except pyodbc.Error as e: 
                        print('Error in Connection', e)
                        signupSuccessful = False

                    if userExists == False:
                        self.setLabelsToDefault(labels=inputLabels)
                        userExists = True
                        if userType == 'Admin':
                            self.signupWarningLbl.config(text='Must Enter Pin,\n For Successful Signup', fg='#7289da')
                            self.authAdmin(username, encryptedPassword, firstname, surname, signedUp)
                        
                        if userType == 'Teacher':
                            self.signupWarningLbl.config(text='Must Enter Subject,\n For Successful Signup', fg='#7289da')
                            self.authTeacher(username, encryptedPassword, firstname, surname, signedUp)
                        
                        if userType == 'Student':
                            self.signupWarningLbl.config(text='Must Enter Subjects,\n For Successful Signup', fg='#7289da')
                            self.authStudent(username, encryptedPassword, firstname, surname, signedUp)
                        
                else:
                    self.signupWarningLbl.config(text='Passwords Do Not Match!', fg='red')
                    self.passwordLbl.config(text='Password', fg='red')
                    self.password2Lbl.config(text='Confirm Password', fg='red')
            else:
                if password != '':
                    self.signupWarningLbl.config(text=f'Password Must Have:{passwordImprovement}', fg='red')
                    self.passwordLbl.config(text='Password', fg='red')
                    self.password2Lbl.config(text='Confirm Password', fg='red')

        return(userExists, signupSuccessful)

#!########################################################################
#!Auth Admin
    def authAdmin(self, username, encryptedPassword, firstname, surname, signedUp):
        popup = tk.Toplevel(self)
        popup.title('Admin Authentication')
        popup.config(bg='#23272a')
        
        popup.focus_set()
        popup.grab_set()

        popupFrame = tk.LabelFrame(popup)
        popupFrame.pack(padx=10, pady=10)

        adminPinLbl = tk.Label(popupFrame, text='Enter Admin Pin:', bg='#23272a', fg='#7289da')
        adminPinLbl.grid(row=1, column=1, padx=20, pady=10)
    
        adminPinEntry = tk.Entry(popupFrame)
        adminPinEntry.grid(row=2, column=1, padx=20, pady=10, sticky='ew')
        adminPinEntry.focus()

        submitBtn = tk.Button(popupFrame, text='Submit', bg='#7289da',
        command=lambda:self.signupAdmin(popup, adminPinEntry, username, encryptedPassword, firstname, surname, signedUp))
        submitBtn.grid(row=3, column=1, padx=20, pady=10, sticky='ew')

        self.adminPinWarning = tk.Label(popupFrame, text='', bg='#23272a')
    
        popup.mainloop()
        return('Admin Auth Process Started')

    def signupAdmin(self, popup, adminPinEntry, username, encryptedPassword, firstname, surname, signedUp):
        adminAuthSuccessful = False
        self.adminPinWarning.grid(row=4, column=1, padx=20, pady=10)

        firstname = firstname.capitalize()
        surname = surname.capitalize()
        newUser = (username, encryptedPassword, firstname, surname, signedUp)

        if adminPinEntry.get().isdigit() == True:
            if adminPinEntry.get() == '123':
                cur.execute('''INSERT INTO 
                            Admin(Username, Password, Firstname, Surname, signedUp) 
                            VALUES(?,?,?,?,?)''', newUser)
                conn.commit()

                self.adminPinWarning.config(text='Correct Admin Pin.', fg='#7289da')
                adminAuthSuccessful = True
                popup.destroy()
                self.delFrames()
                self.loginsys()
            
            else:
                self.adminPinWarning.config(text='Incorrect Admin Pin!', fg='red')
                adminAuthSuccessful = False
        else:
            self.adminPinWarning.config(text='Must Be A Pin!', fg='red')
            adminAuthSuccessful = False

        return(adminAuthSuccessful)
#!########################################################################
#!Auth Teacher
    def authTeacher(self, username, encryptedPassword, firstname, surname, signedUp):
        popup = tk.Toplevel(self)
        popup.title('Teacher Authentication')
        popup.config(bg='#23272a')
        
        popup.focus_set()
        popup.grab_set()

        popupFrame = tk.LabelFrame(popup)
        popupFrame.pack(padx=10, pady=10)

        subjectLbl = tk.Label(popupFrame, text='Enter The Subject You Teach:', bg='#23272a', fg='#7289da')
        subjectLbl.grid(row=1, column=1, padx=20, pady=10)
    
        subjectEntry = tk.Entry(popupFrame)
        subjectEntry.grid(row=2, column=1, padx=20, pady=10, sticky='ew')
        subjectEntry.focus()

        submitBtn = tk.Button(popupFrame, text='Submit', bg='#7289da',
        command=lambda:self.signupTeacher(popup, username, encryptedPassword, firstname, surname, subjectEntry.get(), signedUp))
        submitBtn.grid(row=3, column=1, padx=20, pady=10, sticky='ew')

        self.teacherSubjectWarning = tk.Label(popupFrame, text='', bg='#23272a')
    
        popup.mainloop()
        return('Teacher Auth Process Started')

    def signupTeacher(self, popup, username, encryptedPassword, firstname, surname, subjectEntry, signedUp):
        teacherAuthSuccessful = False
        self.teacherSubjectWarning.grid(row=4, column=1, padx=20, pady=10)

        firstname = firstname.capitalize()
        surname = surname.capitalize()
        subjectEntry = subjectEntry.capitalize()
        newTeacher = (username, encryptedPassword, firstname, surname, subjectEntry, signedUp)

        if subjectEntry != '':
            cur.execute('''INSERT INTO 
                        Teacher(Username, Password, Firstname, Surname, Subject, signedUp) 
                        VALUES(?,?,?,?,?,?)''', newTeacher)
            conn.commit()

            self.teacherSubjectWarning.config(text='Singed Up.', fg='#7289da')
            teacherAuthSuccessful = True
            popup.destroy()
            self.delFrames()
            self.loginsys()
        else:
            self.teacherSubjectWarning.config(text='Enter Information!', fg='red')
            teacherAuthSuccessful = False

        return(teacherAuthSuccessful)
#!########################################################################
#!Auth Student
    def authStudent(self, username, encryptedPassword, firstname, surname, signedUp):
        popup = tk.Toplevel(self)
        popup.title('Student Authentication')
        popup.config(bg='#23272a')
        
        popup.focus_set()
        popup.grab_set()

        popupFrame = tk.LabelFrame(popup)
        popupFrame.pack(padx=10, pady=10)

        cur.execute('select * from Teacher')
        teacherData = []
        for row in cur.fetchall():
            teacherData.append(f'{row[1]} - {row[5]}')

        subject1Lbl = tk.Label(popupFrame, text = 'Subject - Teacher 1')
        subject1Lbl.grid(row = 1, column = 1, padx = 20, pady=(10,0), sticky = 'w')
        subject1Entry = ttk.Combobox(popupFrame, value = teacherData, state='readonly', width = 20) 
        subject1Entry.current(0)
        subject1Entry.grid(row = 2, column = 1, padx=20, pady=(0,10), sticky = 'ew')

        subject2Lbl = tk.Label(popupFrame, text = 'Subject - Teacher 2')
        subject2Lbl.grid(row = 1, column = 2, padx = 20, pady=(10,0), sticky = 'w')
        subject2Entry = ttk.Combobox(popupFrame, value = teacherData, state='readonly', width = 20) 
        subject2Entry.current(0)
        subject2Entry.grid(row = 2, column = 2, padx=20, pady=(0,10), sticky = 'ew')

        subject3Lbl = tk.Label(popupFrame, text = 'Subject - Teacher 3')
        subject3Lbl.grid(row = 1, column = 3, padx = 20, pady=(10,0), sticky = 'w')
        subject3Entry = ttk.Combobox(popupFrame, value = teacherData, state='readonly', width = 20) 
        subject3Entry.current(0)
        subject3Entry.grid(row = 2, column = 3, padx=20, pady=(0,10), sticky = 'ew')

        submitBtn = tk.Button(popupFrame, text='Submit', bg='#7289da',
        command=lambda:self.signupStudent(popup, username, encryptedPassword, firstname, surname, subject1Entry.get(), subject2Entry.get(), subject3Entry.get(), signedUp))
        submitBtn.grid(row=7, column=1, columnspan=3, padx=20, pady=20, sticky='ew')

        self.warning = tk.Label(popupFrame, text='', bg='#23272a')
    
        popup.mainloop()
        return('Student Auth Process Started')

    def signupStudent(self, popup, username, encryptedPassword, firstname, surname, subject1, subject2, subject3, signedUp):
        studentAuthSuccessful = False
        self.warning.grid(row=8, column=1, padx=20, pady=10)

        if subject1 != '' and subject2 != '' and subject3 != '':
            firstname = firstname.capitalize()
            surname = surname.capitalize()
            newStudent = (username, encryptedPassword, firstname, surname, subject1, subject2, subject3, signedUp)

            cur.execute('''INSERT INTO 
                        Student(Username, Password, Firstname, Surname, Subject1, Subject2, Subject3, signedUp) 
                        VALUES(?,?,?,?,?,?,?,?)''', newStudent)
            conn.commit()

            self.warning.config(text='Singed Up.', fg='#7289da')
            studentAuthSuccessful = True
            popup.destroy()
            self.delFrames()
            self.loginsys()

        else:
            self.warning.config(text='Must Enter Subjects', fg='red')
            studentAuthSuccessful = False
        
        return(studentAuthSuccessful)
#!########################################################################
#!toggle password
    def unhideToggleFunc(self, entryBox, toggle, toggleText):
        if entryBox.cget('show') == '•':
            entryBox.config(show='')
            toggleText = 'Hide'
        else:
            entryBox.config(show='•')
            toggleText = 'Un-hide'

        toggle.config(text=toggleText)

        return(f'toggle text changed to: {toggleText}')

#!########################################################################
#!setLabels to default
    def setLabelsToDefault(self, labels):
        for label in (labels):
            newText = label.cget('text')
            label.config(text=newText, fg='#7289da')
        
        return(f'labels set to default: {labels}')

#!########################################################################
#!wipe form content
    def delFrames(self):
        for widget in self.authSysFrame.winfo_children():
            widget.destroy()

        return('wiped authSysFrame clean')
        
#!########################################################################