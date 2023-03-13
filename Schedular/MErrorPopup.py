import tkinter as tk

#!########################################################################
def popup(message):
    popup = tk.Tk()
    popup.title('Warning!')
    popup.config(bg='#23272a')
    popup.geometry('300x100')
    popup.resizable(0, 0)

    tk.Label(popup, text=message, bg='#23272a', fg='red').pack(pady=30)

    popup.mainloop()