import tkinter as tk
from tkinter import *
from tkinter import ttk

from MDBConnection import *
import MData
import StudentDashboard
import TeacherDashboard

#!########################################################################
LargeFont = ('Verdana', 12)

class Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.data = []
        self.taskCount = 0 
        
        self.window = tk.Frame(self)
        self.window.pack(side = 'top', fill = 'both', expand = True)

        self.topFrame = tk.Frame(self.window)
        self.topFrame.pack(fill='x')

        self.label = tk.Label(self.topFrame, text = 'Schedular > Todo List', font=LargeFont)
        self.label.pack(padx=20, pady=10, side='left')

        self.backBtn = tk.Button(self.topFrame, text = 'Back to Dashboard', font=LargeFont, 
        command=lambda:self.back())
        self.backBtn.pack(padx=(5,20), pady=10, side='right')

        self.mainFrame = tk.Frame(self.window, background='#2c2f33')
        self.mainFrame.pack(padx = 20, pady = 10, fill = 'both', expand = True)

        self.createTaskMakerFrame()
        self.createTaskListFrame()
        
#!########################################################################  
    def createTaskMakerFrame(self):
        self.createTaskFrame = tk.Frame(self.mainFrame)
        #createTaskFrame.grid(row=1, column=1, padx=20, pady=10, sticky='nsew')
        self.createTaskFrame.pack(padx=20, pady=10, fill='x')

        self.taskInput = tk.Entry(self.createTaskFrame, font=('Verdana', 14))
        self.taskInput.grid(row=1, column=1, padx=(20,0), pady=10, sticky='ew')
        self.taskInput.bind('<Return>', lambda e: self.addtask(self.taskInput.get()))

        self.submitBtn = tk.Button(self.createTaskFrame, text=' + ', font=LargeFont,
        command= lambda:self.addtask(self.taskInput.get()))
        self.submitBtn.grid(row=1, column=2, padx=(0,20), pady=10, sticky='ew')

        values=['Uncompleted', 'Completed', 'Binned']
        self.filterDropDown = ttk.Combobox(self.createTaskFrame, values=values, font=LargeFont, state='readonly')
        self.filterDropDown.grid(row=1, column=3, padx=20, pady=10, sticky='ew')
        self.filterDropDown.current(0)
        self.filterDropDown.bind('<<ComboboxSelected>>', lambda e: self.filter(self.filterDropDown.get()))

#!########################################################################
    def createTaskListFrame(self):
        self.taskListFrame = tk.Frame(self.mainFrame)
        #self.taskListFrame.grid(row=2, column=1, padx=20, pady=10, sticky='nsew')
        self.taskListFrame.pack(padx=20, pady=10, fill='x')
        
        self.canvas = Canvas(self.taskListFrame, highlightthickness=0)
        self.canvas.pack(side='left', fill='both', expand=1)
        
        self.scrollbar = ttk.Scrollbar(self.taskListFrame, orient='vertical', command=self.canvas.yview)
        self.scrollbar.pack(side='right', fill='y')

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion =self. canvas.bbox("all")))

        self.todoList_subFrame = Frame(self.canvas)

        self.taskListFrame.bind('<Enter>', lambda e: self.bindMouseWheel(e, self.canvas))
        self.taskListFrame.bind('<Leave>', lambda e: self.unbindMouseWheel(e, self.canvas))

        self.canvas.create_window((0,0), window=self.todoList_subFrame, anchor="nw")

#!########################################################################
    def back(self):
        page = StudentDashboard.Page if MData.userType == 'Student' else TeacherDashboard.Page
        self.controller.show_frame(page)
        self.taskInput.delete(0, 'end')
        
        for widget in (self.todoList_subFrame.winfo_children()):
            widget.destroy()

#!##########################################################################
    def addtask(self, task):
        if task != '':
            status = 'Incomplete'
            taskData = (task, status, MData.username, MData.userType)
            self.taskInput.delete(0, 'end')

            cur.execute('INSERT INTO TodoList(Task, Status, Username, UserType) VALUES(?,?,?,?)', taskData)
            conn.commit()

            self.taskCount += 1
            self.filter('Uncompleted')

#!##########################################################################
    def filter(self, filter):
        if filter != '':
            for widget in (self.todoList_subFrame.winfo_children()):
                widget.destroy()

            self.headingLbl = tk.Label(self.todoList_subFrame, text=filter, font=LargeFont)
            self.headingLbl.grid(row=1, column=1, padx=20, pady=10, sticky='w')

            if filter == 'Uncompleted':
                cur.execute('''SELECT * FROM TodoList WHERE Status = 'Incomplete' and Username = ? and UserType = ?''', MData.username, MData.userType)
                for row in cur.fetchall():
                    taskID = row[0]
                    task = row[1]
                    self.taskCount += 1
                    self.taskWidget(taskID=taskID, task=task, btn1text='Complete', btn1func=self.completetask, btn2text='Bin', btn2func=self.bintask)

            if filter == 'Completed':
                cur.execute('''SELECT * FROM TodoList WHERE Status = 'Completed' and Username = ? and UserType = ?''', MData.username, MData.userType)
                for row in cur.fetchall():
                    taskID = row[0]
                    task = row[1]
                    self.taskCount += 1
                    self.taskWidget(taskID=taskID, task=task, btn1text='Not Complete', btn1func=self.incompletetask, btn2text='Bin', btn2func=self.bintask)
            
            if filter == 'Binned':
                cur.execute('''SELECT * FROM TodoList WHERE Status = 'Binned' and Username = ? and UserType = ?''', MData.username, MData.userType)
                for row in cur.fetchall():
                    taskID = row[0]
                    task = row[1]
                    self.taskCount += 1
                    self.taskWidget(taskID=taskID, task=task, btn1text='Complete', btn1func=self.completetask, btn2text='Delete', btn2func=self.deletetask)

#!##########################################################################
    def taskWidget(self, taskID, task, btn1text, btn1func, btn2text, btn2func):
        self.taskFrame = tk.Frame(self.todoList_subFrame, bg = '#23272a')
        self.taskFrame.grid(row = self.taskCount+1, column = 1, padx = 20, pady = (10, 5), sticky = 'ew')
        
        self.btn1 = tk.Button(self.taskFrame, text = btn1text, bg='#2ECC71',
        command = lambda taskFrame= self.taskFrame: btn1func(taskID, task, taskFrame))
        self.btn1.grid(row = 1, column = 1, padx = (10,5), pady = 10, sticky = 'w')

        self.btn2 = tk.Button(self.taskFrame, text = btn2text,
        command = lambda taskFrame= self.taskFrame: btn2func(taskID, task, taskFrame))
        self.btn2.grid(row = 1, column = 2, padx = 0, pady = 10, sticky = 'w')

        self.taskLbl = tk.Label(self.taskFrame, text = task, font = LargeFont)
        self.taskLbl.grid(row = 1, column = 3, padx = 15, pady = 10, sticky = 'w')

#!##########################################################################
    def completetask(self, taskID, task, taskFrame):
        cur.execute('''UPDATE TodoList SET Status = 'Completed' WHERE TaskID = ? and Username = ? and UserType = ?''', taskID, MData.username, MData.userType)
        cur.commit()
        taskFrame.destroy()
        print(f'task: {task}, of task id: {taskID}, Completed')

    def incompletetask(self, taskID, task, taskFrame):
        cur.execute('''UPDATE TodoList SET Status = 'Incomplete' WHERE TaskID = ? and Username = ? and UserType = ?''', taskID, MData.username, MData.userType)
        cur.commit()
        taskFrame.destroy()
        print(f'task: {task}, of task id: {taskID}, Incomplete')

    def bintask(self, taskID, task, taskFrame):
        cur.execute('''UPDATE TodoList SET Status = 'Binned' WHERE TaskID = ? and Username = ? and UserType = ?''', taskID, MData.username, MData.userType)
        cur.commit()
        taskFrame.destroy()
        print(f'task: {task}, of task id: {taskID}, Binned')

    def deletetask(self, taskID, task, taskFrame):
        cur.execute('''DELETE FROM TodoList WHERE TaskID = ? and Username = ? and UserType = ?''', taskID, MData.username, MData.userType)
        cur.commit()
        taskFrame.destroy()
        print(f'task: {task}, of task id: {taskID}, Deleted')

#!########################################################################
    def bindMouseWheel(self, event, canvas):
        canvas.bind_all("<MouseWheel>", lambda e: self._on_mouse_wheel(e, canvas))

    def unbindMouseWheel(self, event, canvas):
        canvas.unbind_all("<MouseWheel>")

    def _on_mouse_wheel(self, event, canvas):#reduce from 120 to increase scroll speed
        canvas.yview_scroll(-1 * int((event.delta / 120)), "units")
