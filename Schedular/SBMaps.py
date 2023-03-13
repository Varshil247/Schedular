import tkinter as tk
from tkintermapview import TkinterMapView

class busMap:
    def __init__(self, frame):
        UK_Long = 53.83052624713114
        UK_Lat = -1.4881471139639921
        self.h = 640
        self.w = 480

        self.mapframe = TkinterMapView(frame, height=self.h, width=self.w)
        self.mapframe.grid(row=2, column=1, padx=20, pady=10, sticky='nsew')

        self.mapframe.set_position(UK_Long, UK_Lat)
        self.mapframe.set_zoom(5)

        self.mapframe.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal

    def placeMarker(self, long, lat, text):
        if long == 53.83052624713114 and lat == 1.4881471139639921: 
            zoom = 5
        else:
            zoom = 10
            
        self.marker = self.mapframe.set_marker(long, lat, text)
        self.mapframe.set_position(long, lat)
        self.mapframe.set_zoom(zoom)

    def placeMarkers(self, slong, slat, stext, dlong, dlat, dtext):
        if slong == 53.83052624713114 and slat == 1.4881471139639921 or dlong == 53.83052624713114 and dlat == 1.4881471139639921: 
            zoom = 5
        else:
            zoom = 10

        self.startMarker = self.mapframe.set_marker(slong, slat, stext)
        self.destMarker = self.mapframe.set_marker(dlong, dlat, dtext)

        self.mapframe.set_position(slong, slat)
        self.mapframe.set_zoom(zoom)

        self.showPath()

    def showPath(self):
        self.mapframe.set_path([self.startMarker.position, self.destMarker.position])