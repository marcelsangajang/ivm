import matplotlib
import numpy as np
from matplotlib import *
from tkinter import *

         
#https://stackoverflow.com/questions/31440167/placing-plot-on-tkinter-main-window-in-python
class Graph:
    def __init__(self):
        """"
        self.window = window
        self.box = Entry(window)
        self.button = Button (window, text="Show graph", command=self.plot)
        self.box.pack ()
        self.button.pack()"""
        
    def mainloop(self):

        #Window
        window = Tk()
        window.geometry('700x400')

    
        """
        #ex = Example(window)
        window.title("Welcome to LikeGeeks app")
        window.geometry('700x400')
          
        #Text
        txt = Entry(window,width=10)
        txt.grid(column=1, row=0)
        
        #Combo box
        combo = Combobox(window)
        combo['values']= (1, 2, 3, 4, 5, "Text")
        combo.current(1) #set the selected item
        combo.grid(column=0, row=1)
        
        #Checkbox 
        chk_state = BooleanVar() 
        chk_state.set(True) #set check state 
        chk = Checkbutton(window, text='Choose', var=chk_state) 
        chk.grid(column=0, row=2)
        
        #Labels and buttons
        lbl = Label(window, text="Hello")
        lbl.grid(column=0, row=3)
        
        def clicked():
            lbl.configure(text="Button was clicked !!")
        
        #Standard buttons
        btn = Button(window, text="Click Me", command=clicked)
        btn.grid(column=2, row=0)
        
        #Radio buttons
        rad1 = Radiobutton(window,text='First', value=1)
        rad2 = Radiobutton(window,text='Second', value=2)
        rad3 = Radiobutton(window,text='Third', value=3)
        rad1.grid(column=0, row=0)
        rad2.grid(column=1, row=0)
        rad3.grid(column=2, row=0)
         
        #Canvas
       
        w = Canvas(window, width=200, height=100)
        w.grid(column=2, row=2)
        w.create_line(0, 0, 200, 100)
        w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
        w.create_rectangle(50, 25, 150, 75, fill="blue")"""
        
        #Main loop
        window.mainloop()
   

    def plot (self):
        x=np.array ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        v= np.array ([16,16.31925,17.6394,16.003,17.2861,17.3131,19.1259,18.9694,22.0003,22.81226])
        p= np.array ([16.23697,     17.31653,     17.22094,     17.68631,     17.73641 ,    18.6368,
            19.32125,     19.31756 ,    21.20247  ,   22.41444   ,  22.11718  ,   22.12453])

        fig = plt.Figure(figsize=(6,6))
        a = fig.add_subplot(111)
        a.scatter(v,x,color='red')
        a.plot(p, range(2 +max(x)),color='blue')
        a.invert_yaxis()

        a.set_title ("Estimation Grid", fontsize=16)
        a.set_ylabel("Y", fontsize=14)
        a.set_xlabel("X", fontsize=14)

        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas.get_tk_widget().pack()
        canvas.draw()  
        
    #https://stackoverflow.com/questions/3925614/how-do-you-read-a-file-into-a-list-in-python
    def read_graph(self, filename):
        #Sample 1 - elucidating each step but not memory efficient
        lines = []
        with open(filename) as file:
            for line in file: 
                line = line.strip().split(' ') #or some other preprocessing
                line = [float(line[0]), float(line[1])]
                lines.append(line) #storing everything in memory!
                
        return lines
