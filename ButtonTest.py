from tkinter import *
from tkinter.ttk import *

class App():    

    def __init__(self, window, window_title, video_source=0):

        self.s = Style()
        self.s.theme_use('alt')

        self.window = window 
        self.window.title(window_title) # Name the window
        self.window.configure(background='black')
        self.s.configure('Panels.TFrame', background='black') 
        self.s.configure('W.TButton', relief="flat", background='black', foreground='red')
        self.s.map('W.TButton', background=[('active', 'yellow')])
        
        pane = Frame(window, style='Panels.TFrame')
        pane.pack(fill = BOTH, expand = True)

        self.btn_lightOn=Button(pane, style='W.TButton', text="Light On", width=50)
        self.btn_lightOn.pack(anchor=CENTER, expand=True)

        self.window.mainloop()

App(Tk(), "Test")