import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from tkinter import *
from tkinter import ttk
import Thesis
import math
from matplotlib.figure import Figure
#https://stackoverflow.com/questions/31440167/placing-plot-on-tkinter-main-window-in-python
#https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/
#Drawing graphs https://www.python-course.eu/tkinter_events_binds.php
class Gui:
    def __init__(self):
        self.calc = Thesis.Calculations()
        self.filename = 'graph1.txt'
        self.points = self.read_graph(self.filename)
        #Calculates all values
        self.data = self.calc.calculate_all(self.points)
        


     
        """"
        self.box = Entry(window)
        self.button = Button (window, text="Show graph", command=self.plot)
        self.box.pack ()
        self.button.pack()"""
        
    def mainloop(self):
        #main window
        window = Tk()
        sizex = 800
        sizey = 600
        window.geometry("%dx%d" % (sizex, sizey))

        titles = ['Index', 'Coords (x, y)', 'RC1', 'RC2', 'Surface from i to i + 1']
        titles2 = ['Graph', 'RC1', 'RC2', 'Surface from i to i + 1']
        width = len(titles)
        height = len(self.points)
        
        table = Frame(window, bg="white", borderwidth=1, relief="solid")
        table.grid(row=0, column=1)
        
        graph = Frame(window, bg="white", borderwidth=1, relief="solid")
        graph.grid(row=0, column=2, sticky=W+E+N+S)
        tabControl = ttk.Notebook(graph)
        
        """Create tabs where graphis are shown"""
        tabs = []
        for i in range(len(self.data)-1):
            tab = ttk.Frame(tabControl, borderwidth=1, relief="raised") # Create a tab 
            #################### 
         
            tabs.append(tab)
            
            fig = Figure(figsize=(6,6))
            a = fig.add_subplot(111)
            temp = self.data[i]
            temp2 = np.array(list(zip(*temp)))
            x = temp2[0]
            y = temp2[1]

            a.plot(x, y,color='blue')
    
            a.set_title (titles2[i], fontsize=16)
            a.set_ylabel("Y", fontsize=14)
            a.set_xlabel("X", fontsize=14)
            
            #a.set_aspect('equal')
            a.grid(True)
            
            a.axhline(y=0, color='k')
            a.axvline(x=0, color='k')
    
            canvas = FigureCanvasTkAgg(fig, tabs[i])
            canvas.get_tk_widget().grid()
            canvas.draw()

            #############
 
            tabControl.add(tab, text=titles2[i])      # Add the tab
        tabControl.grid()  # Pack to make visible
        
        """Create table"""
        #Sets up title column (index)
        for i in range(height):
            text1 = 'i = ' + str(i)
            b = Label(table, text=text1, bg='white')
            b.grid(row=i+1, column=0, sticky=W+E+N+S)
            
        
        #Sets up title row
        for i in range(width):
            b = Label(table, text=titles[i], bg='medium spring green')
            b.grid(row=0, column=i, sticky=W+E+N+S)
            
        for i in range(width):
            #setup column for x-coord
            if i == 0:
                b = Label(table, text='', bg='white', borderwidth=1, relief="sunken")
                b.grid(row=1, column=i+1, sticky=W+E+N+S)
                continue
            
            #setup columns for resulting data
 
            for j in range(height): #Rows
                b = Label(table, text='', bg='white', borderwidth=1, relief="sunken")
                b.grid(row=j+1, column=i+1, sticky=W+E+N+S)
                
        #button action
        def clicked():
            self.calc_all(table, tabs)
    
        #Standard buttons
        btn = Button(window, text="Calculate all", command=clicked, bg="cyan")
        btn.grid(column=0, row=0, sticky=N)
        
        self.calc_all(table, tabs)
        

        
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
   
    def calc_all(self, table, tabs):       

        
        self.update_table(table)
        self.update_tabs(tabs)
    
    def update_table(self, table):
        data = self.data
        
        """"""
        width = len(data)
        height = len(data[0])
    
        for i in range(width):
            height = len(data[i])
            #setup column for x-coord
            if i == 0:
                for j in range(height): #Rows
                    x = round(data[i][j][0], 3)
                    y = round(data[i][j][1], 3)
                    text1 = '(' + repr(x) + ', ' + repr(y) + ')'
                    b = Label(table, text=text1, bg='white', borderwidth=1, relief="sunken")
                    b.grid(row=j+1, column=i+1, sticky=W+E+N+S)
                    
                continue
            
            #setup columns for resulting data
 
            for j in range(height): #Rows
                y = round(data[i][j][1], 3)
                b = Label(table, text=y, bg='white', borderwidth=1, relief="sunken")
                b.grid(row=j+1, column=i+1, sticky=W+E+N+S)
                

    def update_tabs(self, tabs):
        pass
        
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

if __name__ == '__main__':
    g = Gui()
    g.mainloop()
 