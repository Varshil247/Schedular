import tkinter as tk
from tkinter import ttk

import requests
import MData
import StudentDashboard
import TeacherDashboard
import SBMaps

#!########################################################################
LargeFont = ('Verdana', 12)

class Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.startLocationName = ''
        self.startLocationID = ''
        self.startLocationCoords = [1.4881471139639921,53.83052624713114]

        self.destLocationName = ''
        self.destLocationID = ''
        self.destLocationCoords = [1.4881471139639921,53.83052624713114]

        self.window = tk.Frame(self)
        self.window.pack(side = 'top', fill = 'both', expand = True)
        
        self.topFrame = tk.Frame(self.window)
        self.topFrame.pack(fill='x')

        self.logo = tk.Label(self.topFrame, text = 'Schedular > Track Busses', font=LargeFont)
        self.logo.pack(padx=20, pady=10, side='left')

        self.backBtn = tk.Button(self.topFrame, text = 'Back to Dashboard', font=LargeFont, 
        command=lambda: self.back())
        self.backBtn.pack(padx=(5,20), pady=10, side='right')

        self.mainFrame = tk.Frame(self.window, bg = '#2c2f33')
        self.mainFrame.pack(padx = 20, pady = 10, fill='both', expand=True)

        self.searchBussesFrame()
        self.viewStops()
        self.viewBusses()

#!########################################################################
    def back(self):
        page = StudentDashboard.Page if MData.userType == 'Student' else TeacherDashboard.Page
        self.controller.show_frame(page)

#!########################################################################
    def searchBussesFrame(self):
        self.searchFrame = tk.Frame(self.mainFrame)
        self.searchFrame.grid(row=1, column=1, padx=20, pady=10, sticky='nsew')

        self.startSearchFrame = tk.LabelFrame(self.searchFrame, text='Choose Start Location')
        self.startSearchFrame.grid(row=1, column=1, padx=20, pady=10, sticky='ew')

        self.startInput = tk.Entry(self.startSearchFrame, font=LargeFont, width=35)
        self.startInput.grid(row=1, column=1, padx=(5,0), pady=5, sticky='ew')
        self.startInput.bind('<Return>', lambda e: self.searchStop(stopQuery=self.startInput.get(), entry=self.startInput))

        self.startSearchBtn = tk.Button(self.startSearchFrame, text='🔍', font=('Verdana', 10),
        command=lambda: self.searchStop(stopQuery=self.startInput.get(), entry=self.startInput))
        self.startSearchBtn.grid(row=1, column=2, padx=(0,5), pady=5, sticky='ew')

        self.destSearchFrame = tk.LabelFrame(self.searchFrame, text='Choose Destination Location')
        self.destSearchFrame.grid(row=2, column=1, padx=20, pady=10, sticky='ew')

        self.destInput = tk.Entry(self.destSearchFrame, font=LargeFont, width=35)
        self.destInput.grid(row=1, column=1, padx=(5,0), pady=5, sticky='ew')
        self.destInput.bind('<Return>', lambda e: self.searchStop(stopQuery=self.destInput.get(), entry=self.destInput))

        self.destSearchBtn = tk.Button(self.destSearchFrame, text='🔍', font=('Verdana', 10),
        command=lambda: self.searchStop(stopQuery=self.destInput.get(), entry=self.destInput))
        self.destSearchBtn.grid(row=1, column=2, padx=(0,5), pady=5, sticky='ew')
        
#!########################################################################    
    def searchStop(self, stopQuery, entry):
        self.resultFrame = tk.Frame(self.searchFrame)
        self.resultFrame.grid(row=3, column=1, padx=20, pady=10, sticky='nsew')

        self.canvas = tk.Canvas(self.resultFrame, highlightthickness=0)
        self.canvas.grid(row = 1, column = 1, padx = 20, pady = 10, sticky = 'nsew')
        
        self.busStopList_subFrame = tk.Frame(self.canvas)

        self.scrollbar = ttk.Scrollbar(self.resultFrame, orient='vertical', command=self.canvas.yview)
        self.scrollbar.grid(row = 1, column = 2, sticky = 'ns')

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all")))
        self.busStopList_subFrame.bind('<Enter>', lambda e: self.bindMouseWheel(e, self.canvas))
        self.busStopList_subFrame.bind('<Leave>', lambda e: self.unbindMouseWheel(e, self.canvas))

        self.canvas.create_window((0,0), window=self.busStopList_subFrame, anchor="nw")

        for stop in self.busStopList_subFrame.winfo_children():
            stop.destroy()

        busStopRes = requests.get(f'http://transportapi.com/v3/uk/places.json?query={stopQuery}&app_id=820b3071&app_key=a614989938d327d49ba024b77a0f757a&group=route&nextbuses=yes')
        busStopRes.close()
        data = busStopRes.json()

        for i in range(len(data['member'])):
            if 'atcocode' in data['member'][-1+i]:
                stopName = data['member'][-1+i]['name']
                stopDescription = data['member'][-1+i]['description']
                stopID = data['member'][-1+i]['atcocode']
       
                self.busStopBtn = tk.Button(self.busStopList_subFrame, text = stopName+'\n'+stopDescription, height=3, width=45,
                command = lambda stopID = stopID, entry=entry: self.setStop(stopID, entry))
                self.busStopBtn.grid(row = i, column = 1, padx = 0, pady = (10,0), sticky = 'w')

    def setStop(self, StopID, entry):
        focusedBusStopRes = requests.get(f'http://transportapi.com//v3/uk/bus/stop/{StopID}/live.json?app_id=820b3071&app_key=a614989938d327d49ba024b77a0f757a&group=route&nextbuses=yes')
        focusedBusStopRes.close()
        data = focusedBusStopRes.json()

        stopName = data['name']
        stopLoc = data['location']['coordinates']
        stopType = 'Start'

        if entry == self.startInput:
            self.startLocationName = stopName#StopID
            self.startLocationID = StopID
            self.startLocationCoords = stopLoc
            stopType = 'Start'
            self.showBusses(data)
        if entry == self.destInput:
            self.destLocationName = stopName#StopID
            self.destLocationID = StopID
            self.destLocationCoords = stopLoc
            stopType = 'Destination'

        entry.delete(0, 'end')
        entry.insert(0, stopName)
        for stop in self.busStopList_subFrame.winfo_children():
            stop.destroy()

        SBMaps.busMap(frame=self.viewStopsFrame).placeMarker(long=stopLoc[1], lat=stopLoc[0], text=stopType+': '+stopName)
#!########################################################################
    def viewStops(self):
        self.viewStopsFrame = tk.Frame(self.mainFrame)
        self.viewStopsFrame.grid(row=1, column=2, padx=20, pady=10, sticky='nsew')

        self.startSearchBtn = tk.Button(self.viewStopsFrame, text='View Start And Destination Bus Stops.',
        command=lambda: self.showStops(start=self.startLocationName, dest=self.destLocationName, mapFrame=self.viewStopsFrame))
        self.startSearchBtn.grid(row=1, column=1, padx=20, pady=10, sticky='ew')

    def showStops(self, start, dest, mapFrame):
        print(start ,'-->', dest)
        SBMaps.busMap(frame=mapFrame)
        SBMaps.busMap(frame=mapFrame).placeMarkers(slong=self.startLocationCoords[1], slat=self.startLocationCoords[0], stext='Start: '+ start,
                                                dlong=self.destLocationCoords[1], dlat=self.destLocationCoords[0], dtext='Destination: '+ dest)

#!########################################################################
    def viewBusses(self):
        self.viewBussesFrame = tk.Frame(self.mainFrame)
        self.viewBussesFrame.grid(row=1, column=3, padx=20, pady=10, sticky='nsew')
        
        self.startBussesLbl = tk.Label(self.viewBussesFrame, text='Busses At Start Location: ', width=35)
        self.startBussesLbl.grid(row=1, column=1, padx=20, pady=10, sticky='nsew')

    def showBusses(self, data):
        self.resultFrame = tk.Frame(self.viewBussesFrame)
        self.resultFrame.grid(row=2, column=1, padx=20, pady=10, sticky='nsew')

        self.canvas = tk.Canvas(self.resultFrame, highlightthickness=0)
        self.canvas.grid(row = 1, column = 1, padx = 20, pady = 10, sticky = 'nsew')
        
        self.bussesList_subFrame = tk.Frame(self.canvas)

        self.scrollbar = ttk.Scrollbar(self.resultFrame, orient='vertical', command=self.canvas.yview)
        self.scrollbar.grid(row = 1, column = 2, sticky = 'ns')

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all")))
        self.bussesList_subFrame.bind('<Enter>', lambda e: self.bindMouseWheel(e, self.canvas))
        self.bussesList_subFrame.bind('<Leave>', lambda e: self.unbindMouseWheel(e, self.canvas))

        self.canvas.create_window((0,0), window=self.bussesList_subFrame, anchor="nw")

        rowCount = 0
        self.startBussesLbl.config(text=f'Busses At {self.startLocationName} (Start Location):')
        for i in data['departures']:
            rowCount += 1
            line = data['departures'][i][0]['line']
            direction = data['departures'][i][0]['direction']
            operator = data['departures'][i][0]['operator']
            aimedDepTime = data['departures'][i][0]['aimed_departure_time']
            
            self.busBtn = tk.Button(self.bussesList_subFrame, text = line+'\n'+direction+'\n'+operator+'\n'+aimedDepTime, height=5, width=45)
            self.busBtn.grid(row = 3+rowCount, column = 0, padx = 10, pady = (10,0), sticky = '')

#!########################################################################
    def bindMouseWheel(self, event, canvas):
        canvas.bind_all("<MouseWheel>", lambda e: self._on_mouse_wheel(e, canvas))

    def unbindMouseWheel(self, event, canvas):
        canvas.unbind_all("<MouseWheel>")

    def _on_mouse_wheel(self, event, canvas):#reduce from 120 to increase scroll speed
        canvas.yview_scroll(-1 * int((event.delta / 120)), "units")
        
