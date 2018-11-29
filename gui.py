import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from tkinter import *
from tkinter import ttk
import Thesis
import math
from matplotlib.figure import Figure
import os
import re
#https://stackoverflow.com/questions/31440167/placing-plot-on-tkinter-main-window-in-python
#https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/
#Drawing graphs https://www.python-course.eu/tkinter_events_binds.php
class Gui:
    def __init__(self):
        self.calc = Thesis.Calculations()
        self.filename = '1'
        self.filepath = './graphs/'
        self.files = []
        self.points = []#self.read_graph(self.filename)
        #Calculates all values
        self.data = [] #= #self.calc.calculate_all(self.points)
        self.w_canvas = 500
        self.h_canvas = 500
        
    def mainloop(self):
        #main window
        window = Tk()
        sizex = 1400
        sizey = 1000
        window.geometry("%dx%d" % (sizex, sizey))

        titles = ['Index', 'Coords (x, y)', 'RC1', 'RC2', 'Surface from i to i + 1']
        titles2 = ['Graph', 'RC1', 'RC2', 'Surface from i to i + 1']
        width = len(titles)
        height = len(self.points)
        
        """Create graph choie menu"""
        menu = Frame(window, bg="white", borderwidth=1, relief="solid")
        menu.grid(row=0, column=0, sticky=N)
        table = Frame(window, bg="white", borderwidth=1, relief="solid")
        table.grid(row=0, column=1)
        
        b = Label(menu, text="Kies een grafiek", bg='medium spring green')
        b.grid(row=0, sticky=N+E+S+W)
        
        def load_graph(filename):
            print('load-graph')
            print(filename)
            self.filename = filename
            self.points = self.read_graph(filename)
            self.data = self.calc.calculate_all(self.points)
            self.update_table(table)

        
        graph_list = self.files
        def update_menu():
            
            files = []
            #Find all txt files, creates a non-taken name
            for file in os.listdir(self.filepath):
                if file.endswith(".txt"):
                    temp = re.sub("\D", "", file)
                    if len(temp) > 0:
                        files.append(int(temp))
            #Find files
            self.files = files
            
            #Create buttons
            for i in range(len(files)):
                #Create graph choie menu
                btn = Button(menu, text='Graph '+str(files[i]), command=load_graph(files[i]), bg='PaleTurquoise2')
                btn.grid(row = i, column = 0, sticky=W+E+N+S)
            

        
        update_menu()
            
        """Left box (table)"""

        #Sets up title column (index)
        for i in range(height):
            text1 = 'i = ' + str(i)
            b = Label(table, text=text1, bg='white')
            b.grid(row=i+3, column=0, sticky=W+E+N+S)
            
        
        #Sets up title row
        for i in range(width):
            b = Label(table, text=titles[i], bg='medium spring green')
            b.grid(row=2, column=i, sticky=W+E+N+S)
            
        for i in range(width):
            #setup column for x-coord
            if i == 0:
                b = Label(table, text='', bg='white', borderwidth=1, relief="sunken")
                b.grid(row=3, column=i+1, sticky=W+E+N+S)
                continue
            
            #setup columns for resulting data
 
            for j in range(height): #Rows
                b = Label(table, text='', bg='white', borderwidth=1, relief="sunken")
                b.grid(row=j+3, column=i+1, sticky=W+E+N+S)
                
        
        """Mid box (tabs where graphis are shown)"""
        box_mid = Frame(window, bg="white", borderwidth=1, relief="solid")
        box_mid.grid(row=0, column=2, sticky=W+E+N+S)
        tabControl = ttk.Notebook(box_mid)
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
        
        """Right box (input and graph management)"""
        box_right = Frame(window, bg="white", borderwidth=1, relief="solid")
        box_right.grid(row=0, column=3, sticky=W+E+N+S)

        
        points_drawing = []
        
        spline = 0
        
        tag1 = "theline"
        
        def point(event):
        	c.create_oval(event.x, event.y, event.x+1, event.y+1, fill="black")
        	points_drawing.append(event.x)
        	points_drawing.append(event.y)
        	return points_drawing
        
        def canxy(event):
        	print(event.x, event.y)
        
        def graph(event):
        	global theline
        	c.create_line(points_drawing, tags="theline")
        	
        
        def toggle(event):
        	global spline
        	if spline == 0:
        		c.itemconfigure(tag1, smooth=1)
        		spline = 1
        	elif spline == 1:
        		c.itemconfigure(tag1, smooth=0)
        		spline = 0
        	return spline
        
        
        c = Canvas(box_right, bg="white", width=self.w_canvas, height=self.h_canvas)
        
        c.configure(cursor="crosshair")
        
        c.grid()
        
        c.bind("<B1-Motion>", point)
        
        c.bind("<Button-3>", graph)
        
        c.bind("<Button-2>", toggle)
        
        
        #button action
        def clicked():
            #self.calc_all(table, tabs)
            print(points_drawing)
            
        #button action
        def clicked2():
            #self.calc_all(table, tabs)
            c.delete("all")
            points_drawing.clear()
            
        #Stores drawing as file
        def clicked3():
            self.save_graph(points_drawing)   
            update_menu(menu)
                        
        #Standard buttons
        btn = Button(box_right, text="Print", command=clicked, bg='medium spring green')
        btn.grid(sticky=E)
        
        btn = Button(box_right, text="Clear", command=clicked2, bg='medium spring green')
        btn.grid(sticky=E)
        
        btn = Button(box_right, text="Save", command=clicked3, bg='medium spring green')
        btn.grid(sticky=E)
        
        #self.calc_all(table, tabs)
        
        #Main loop
        window.mainloop()
   
    def save_graph(self, points_drawing):
        #rewrite format of the file
        text = str(points_drawing)
        text = re.sub('[^0-9.]', ' ', text).lstrip()
 
        print('points drawing---------')
        print(points_drawing)
        print('text---------')
        print(text)
        
        files = []
        #Find all txt files, creates a non-taken name
        for file in os.listdir(self.filepath):
            if file.endswith(".txt"):
                temp = re.sub("\D", "", file)
                if len(temp) > 0:
                    files.append(int(temp))
        
        temp = text.split()
        #Iterates though X coords (= every 2nd number in txt file)
        string = ""  
        i = 0
        while i < len(temp) - 4:
            counter = 1
            x = float(temp[i])
            y = float(temp[i + 1])
            #checks right nieghbour coords if x value is same
            j = i + 2
            while float(temp[j]) == x:
                y += float(temp[j + 1])
                j += 2
                counter += 1

            if counter != 1:
                y = self.h_canvas - y / counter
            
            i = j  
            string += str(x) + ' ' + str(y) + ' '
        
        #Create unique name for file
        for i in range(100):
            duplicate = False
            for j in range(len(files)):
                if i == files[j]:
                    duplicate = True
                    break
            
            if duplicate == False:
                #create file with name i
                f = open(self.filepath + str(i) + '.txt', "x")
                f.write(string)
                return
                
        print('max limit of files is 100')
        
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
                    b.grid(row=j+3, column=i+1, sticky=W+E+N+S)
                    
                continue
            
            #setup columns for resulting data
 
            for j in range(height): #Rows
                y = round(data[i][j][1], 3)
                b = Label(table, text=y, bg='white', borderwidth=1, relief="sunken")
                b.grid(row=j+3, column=i+1, sticky=W+E+N+S)
                

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
        name = self.filepath + str(filename) + '.txt'
        lines = []

        with open(name) as file:
       
            for j in file:
  
                temp = j.strip().split()
       
                for i in range(len(temp)):
                    if i % 2 == 0:
                        x = temp[i]
                    elif i % 2 == 1:
                        y = temp[i]
                        #print('({},{})'.format(x,y))

                        try:
                            line = [float(x), float(y)]
                            lines.append(line) #storing everything in memory!
                        except:
                            pass
                            #print('error while reading file')
     
 
        return lines

if __name__ == '__main__':
    g = Gui()
    g.mainloop()
 