import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from tkinter import *
from tkinter import ttk
import tkinter as tk
import Thesis
import math
from matplotlib.figure import Figure
import os
import re
#https://stackoverflow.com/questions/31440167/placing-plot-on-tkinter-main-window-in-python
#https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/
#Drawing graphs https://www.python-course.eu/tkinter_events_binds.php
#https://gist.github.com/EugeneBakin/76c8f9bcec5b390e45df scrollframe
#https://stackoverflow.com/questions/17125842/changing-the-text-on-a-label
#https://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-group-of-widgets-in-tkinter/3092341#3092341
class Example(tk.Frame):
    def __init__(self, root):

        tk.Frame.__init__(self, root)
        self.canvas = tk.Canvas(root, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.frame.grid(sticky=N+E+S+W)
        self.vsb = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.grid(row=0, column = 0,sticky=E+N+S)
        self.canvas.grid(row=0, column = 0, sticky=N+W+S+E)
        self.canvas.create_window((8,8), window=self.frame, anchor="nw", 
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

  

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def update_table(self, data, titles):         
        scrollbar = self.frame
        table_w = len(data) #+1 for index column
        table_h = len(data[0]) #+1 for title row
        #Sets up title row
        for i in range(len(titles)):
            b = Label(scrollbar, text=titles[i], bg='medium spring green')
            b.grid(row=0, column=i, sticky=W+E+N+S)
           # table_conten[i].append(b)
        
        #Sets up title column (index)
        for i in range(table_h):
            text1 = 'i = ' + str(i)
            b = Label(scrollbar, text=text1, bg='white')
            b.grid(row=i+1, column=0, sticky=W+E+N+S)
            #table_conten[0].append(b)
          
        #Creates rows for Y, RC1, RC2
        for i in range(table_w):            
            height = len(data[i])
            
            for j in range(height): #Rows
                y = round(data[i][j], 3)
                b = Label(scrollbar, text=y, bg='white', borderwidth=1, relief="sunken")
                b.grid(row=j+1, column=i+1, sticky=W+E+N+S)
 
class Gui:
    def __init__(self, root):
        self.calc = Thesis.Calculations()
        self.filename = '1'
        self.filepath = './graphs/'
        self.files = []
        self.points = []#self.read_graph(self.filename)
        #Calculates all values
        self.data = [] #= #self.calc.calculate_all(self.points)
        self.w_canvas = 500
        self.h_canvas = 500
        self.inp = None
        self.titles_table = ['Index', 'X', 'Y', 'RC1', 'RC2']
        self.titles_tabs = ['Origrinal graph', 'RC1', 'RC2']
        self.table_h = 20
        self.table_w = len(self.titles_table)
        
     
        self.ratio_table = []
        #main window
        self.window = root
        self.window.grid()
        self.sizex = 1400
        self.sizey = 1000
        #self.window.geometry("%dx%d" % (self.sizex, self.sizey))
 
        """Frame for menu menu"""

        self.menu = Frame(self.window, borderwidth=1, relief="solid")
        self.menu.grid(column=0, sticky=N+E+W)
        
        """menu 1"""
        self.menu1 = Frame(self.menu, bg="spring green", borderwidth=1, relief="solid")
        self.menu1.grid(row=0, sticky=N+E+S+W)
                
        #self.menu_label1 = Label(self.menu1, bg="spring green", text="Input options:")
        #self.menu_label1.grid(row=0, column=0, sticky=N+E+S+W)
        
        self.menu_label2 = Label(self.menu1, bg="spring green", text="Choose graph")
        self.menu_label2.grid(row=2, column=0, sticky=N+E+S+W)
        self.input = Entry(self.menu1, text="")
        self.input.grid(row=2, column=1)
        
        self.input_button = Button(self.menu1, text="Load graph", command=self.load_graph, bg='green3')
        self.input_button.grid(row = 3, columnspan = 2, sticky=N+E+S+W)
        
        self.input_button2 = Button(self.menu1, text="Apply algorithm", command=self.algorithm, bg='steelblue3')
        self.input_button2.grid(row=4, columnspan = 2, sticky=N+E+S+W)
        
        self.input_button3 = Button(self.menu1, text="Draw graph", command=self.drawing, bg='mediumorchid3')
        self.input_button3.grid(row=6, columnspan = 2, sticky=W+N+S+E)
        
        
        """menu 2"""
        #self.menu2 = Frame(self.menu, borderwidth=1, relief="solid" , bg='steelblue1')
        #self.menu2.grid(row=1,  sticky=N+E+S+W)
        
        #self.menu_label3 = Label(self.menu2, text="Output options:", bg='steelblue1')
        #self.menu_label3.grid(row=1)
        #self.input_button2 = Button(self.menu2, text="Apply algorithm", command=self.algorithm, bg='steelblue3')
        #self.input_button2.grid(row=2, columnspan = 2, sticky=N+E+S+W)
        
        """menu 3"""
        #self.menu3 = Frame(self.menu, borderwidth=1, relief="solid" , bg='mediumorchid1')
        #self.menu3.grid(row=2,  sticky=N+E+S+W)
        
       # self.menu_label4 = Label(self.menu3, text="Drawing options:", bg='mediumorchid1')
        #self.menu_label4.grid(row=1)
        #self.input_button3 = Button(self.menu3, text="Draw graph", command=self.drawing, bg='mediumorchid3')
        #self.input_button3.grid(row=2, column = 0, sticky=W)
        
        """Frame for table"""
        self.table = Frame(self.window, bg="white", borderwidth=1, relief="solid")
        self.table.grid(row=0, column=1, sticky=N+E+W+S)
        #self.scrollb = Example(self.table)
        #self.scrollb.grid()

        
        """Frame for graphs (tabs where graphis are shown)"""
        self.box_mid = Frame(self.window, bg="white", borderwidth=1, relief="solid")
        self.box_mid.grid(row=0, column=2, sticky=W+E+N+S)
        
        """Frame for drawing"""
        #self.box_right = Frame(self.window, bg="white", borderwidth=1, relief="solid")
        #self.box_right.grid(row=0, column=3, sticky=W+E+N+S)
                
    def algorithm(self):
        
        main_titles = []
 
        

        
        #Window
        w = Tk()
        w.grid()
     
        l = Label(w, bg="spring green", text="Calculate for N")
        l.grid(row=0, column=0, sticky=N+S+W)
        self.inp = Entry(w, text="")
        self.inp.grid(row=0, column=0)
        
        t = Frame(w, bg="white", borderwidth=1, relief="solid")
        t.grid(sticky=N+E+W+S)
        e = Example(t)
        e.grid()
        #self.assess(e, 5, 0.6, 0.25)
        #Buttons
        input_button = Button(w, text="Calculate:", command=self.assess(e, t), bg='mediumorchid3')
        input_button.grid(row=0, column=0, sticky=E)
        
        w.mainloop()
        #Table


        
        
        
        
    def assess(self, root, t):
        n_size = 5
        neg_limit = 0.6
        total_limit = 0.25
        n_size = self.inp.get()
        print('in assess')
        titles = ['Index', 'Verhouding B - S', 'Oppervlakte ratio ']
        rc2_list = self.data[len(self.data) - 1]
        ratios = self.calc.algorithm(self.x, rc2_list, n_size)
        answer = self.calc.assessment(ratios, neg_limit, total_limit)
        self.ratio_table.append(ratios[0])
        self.ratio_table.append(ratios[1])
        #self.ratio_table.append(answer[1])
        root.grid_forget()
        root.destroy()
        root = Example(t)
        root.grid()
        root.update_table(self.ratio_table, titles)
        root.update()
       
   
    def load_graph(self):
        temp = self.input.get()
        if len(temp) > 0:
            self.filename = temp
            self.points = self.read_graph(self.filename)
            self.data = self.calc.calculate_all(self.points)
            self.table_h = len(self.data[0])
            
            #Table
            self.table.grid_forget()
            self.table.destroy()
            self.table = Frame(self.window, bg="white", borderwidth=1, relief="solid")
            self.table.grid(row=0, column=1, sticky=N+E+W+S)
            e = Example(self.table)
            e.grid()
            e.update_table(self.data, self.titles_table)
      
            #Tabs and graphs
            self.box_mid.grid_remove()
            self.box_mid.destroy()
            self.box_mid = Frame(self.window, bg="white", borderwidth=1, relief="solid")
            self.box_mid.grid(row=0, column=2, sticky=W+E+N+S)
            self.x = self.data[0]
            y_coords = self.data[1:]
            self.update_graphs(self.box_mid, self.x, y_coords, self.titles_tabs)
        else:
            print('niks ingevuld')
              
#        self.update_graphs()
        """
    def create_menu(self, master):
        btns = []
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
            btn = Button(master, text='Graph '+str(files[i]), command=self.load_graph(self.files[i]), bg='PaleTurquoise2')
            btn.grid(sticky=W+E+N+S)
            btns.append(btn)
        return btns
    """
    """Table"""
    
    def drawing(self):
        print('in drawing')
        """Drawings"""        
        root = Tk()
        root.grid()
        points_drawing = []
        spline = 0 
        tag1 = "theline"
        
        def point(event):
        	c.create_oval(event.x, event.y, event.x+1, event.y+1, fill="black")
        	points_drawing.append(event.x)
        	points_drawing.append(event.y)
        	return points_drawing
        
        c = Canvas(root, bg="white", width=self.w_canvas, height=self.h_canvas)       
        c.configure(cursor="crosshair")       
        c.grid(row=0)     
        c.bind("<B1-Motion>", point)
        
        def clicked2():
            #self.calc_all(table, tabs)
            c.delete("all")
            points_drawing.clear()
            
        #Stores drawing as file
        def clicked3():
            self.save_graph(points_drawing)   
            points_drawing.clear()
            #update_menu(menu_buttons)
                        
        btn = Button(root, text="Clear", command=clicked2, bg='medium spring green')
        btn.grid(row=1, sticky=N+W+S)
        btn = Button(root, text="Save", command=clicked3, bg='medium spring green')
        btn.grid(row=1, sticky=N+E+S)
    
    def update_graphs(self, root, x, y_coords, titles):
        #Connect to root
        tab_control = ttk.Notebook(root)
        """Graphs (tabs)"""
        for i in range(len(y_coords)):
            #Create tab
            tab = ttk.Frame(tab_control, borderwidth=1, relief="raised")
                 
            self.plot(tab, x, y_coords[i], titles[i])
            x = x[:-1]
            #add tab
            tab_control.add(tab, text=titles[i])    
        tab_control.grid()  # grid to make visible
        
    def plot(self, root, x, y, title):
        if len(x) != len(y):
            print('verkeerde lengte')
            return
        
        fig = Figure(figsize=(6,6))
        a = fig.add_subplot(111)
       
        a.plot(x, y,color='blue')
        a.set_title (title, fontsize=16)
        a.set_ylabel("Y", fontsize=14)
        a.set_xlabel("X", fontsize=14)
        #a.set_aspect('equal')
        a.grid(True)
        a.axhline(y=0, color='k')
        a.axvline(x=0, color='k')

        canvas = FigureCanvasTkAgg(fig, root)
        canvas.get_tk_widget().grid()
        canvas.draw()
      
    def save_graph(self, points_drawing):
        #rewrite format of the file
        text = str(points_drawing)
        text = re.sub('[^0-9.]', ' ', text).lstrip()
 
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
                y =  (y / counter)
                
                
            y = self.h_canvas - y
            i = j  
            string += str(x) + ' ' + str(y) + ' '
        print(string)
        
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
    root = Tk()
    g = Gui(root)
    root.mainloop()
 