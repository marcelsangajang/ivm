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
#https://gist.github.com/EugeneBakin/76c8f9bcec5b390e45df scrollframe
#https://stackoverflow.com/questions/17125842/changing-the-text-on-a-label
#https://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-group-of-widgets-in-tkinter/3092341#3092341

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
        
        self.titles = ['Index', 'X', 'Y', 'RC1', 'RC2', 'Surface i to i + 1: Total || breder || smaller ']
        self.titles_tabs = ['Origrinal graph', 'RC1', 'RC2']
        self.table_h = 20
        self.table_w = len(self.titles)
        
     
           
        #main window
        self.window = Tk()
        self.sizex = 1400
        self.sizey = 1000
        self.window.geometry("%dx%d" % (self.sizex, self.sizey))

        self.width = len(self.titles)
        self.height = 20#len(self.points)
        
        """Frame for menu menu"""

        self.menu = Frame(self.window, borderwidth=1, relief="solid")
        self.menu.grid(column=0, sticky=N+E+W)
        
        """menu 1"""
        self.menu1 = Frame(self.menu, bg="spring green", borderwidth=1, relief="solid")
        self.menu1.grid(row=0, sticky=N+E+S+W)
                
        self.menu_label1 = Label(self.menu1, bg="spring green", text="Input options:")
        self.menu_label1.grid(row=0, column=0, sticky=N+E+S+W)
        
        self.menu_label2 = Label(self.menu1, bg="spring green", text="Choose graph")
        self.menu_label2.grid(row=2, column=0, sticky=N+E+S+W)
        self.input = Entry(self.menu1, text="")
        self.input.grid(row=2, column=1)
        
        self.input_button = Button(self.menu1, text="Load graph", command=self.load_graph, bg='green3')
        self.input_button.grid(row = 3, columnspan = 2, sticky=N+E+S+W)
        
        """menu 2"""
        self.menu2 = Frame(self.menu, borderwidth=1, relief="solid" , bg='steelblue1')
        self.menu2.grid(row=1,  sticky=N+E+S+W)
        
        self.menu_label3 = Label(self.menu2, text="Output options:", bg='steelblue1')
        self.menu_label3.grid(row=1)
        self.input_button2 = Button(self.menu2, text="Apply algorithm", command=self.algorithm, bg='steelblue3')
        self.input_button2.grid(row=2, columnspan = 2, sticky=N+E+S+W)
        
        """menu 3"""
        self.menu3 = Frame(self.menu, borderwidth=1, relief="solid" , bg='mediumorchid1')
        self.menu3.grid(row=2,  sticky=N+E+S+W)
        
        self.menu_label4 = Label(self.menu3, text="Drawing options:", bg='mediumorchid1')
        self.menu_label4.grid(row=1)
        self.input_button3 = Button(self.menu3, text="Clear drawing", command='', bg='mediumorchid3')
        self.input_button3.grid(row=2, column = 0, sticky=W)
        self.input_button4 = Button(self.menu3, text="Save drawing", command='', bg='mediumorchid3')
        self.input_button4.grid(row=2, column= 1, sticky=E)
        
        """Frame for table"""
        self.table = Frame(self.window, bg="white", borderwidth=1, relief="solid")
        self.table.grid(row=0, column=1, sticky=N+E+W+S)
        
        """Frame for graphs (tabs where graphis are shown)"""
        self.box_mid = Frame(self.window, bg="white", borderwidth=1, relief="solid")
        self.box_mid.grid(row=0, column=2, sticky=W+E+N+S)
        
        """Frame for drawing"""
        self.box_right = Frame(self.window, bg="white", borderwidth=1, relief="solid")
        self.box_right.grid(row=0, column=3, sticky=W+E+N+S)

        
    def mainloop(self):


        """Drawings"""        
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
        
        
        c = Canvas(self.box_right, bg="white", width=self.w_canvas, height=self.h_canvas)
        
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
            points_drawing.clear()
            #update_menu(menu_buttons)
                        
        #Standard buttons
        btn = Button(self.box_right, text="Print", command=clicked, bg='medium spring green')
        btn.grid(sticky=E)
        
        btn = Button(self.box_right, text="Clear", command=clicked2, bg='medium spring green')
        btn.grid(sticky=E)
        
        btn = Button(self.box_right, text="Save", command=clicked3, bg='medium spring green')
        btn.grid(sticky=E)
        
        #self.calc_all(table, tabs)
        
        #Main loop
        self.window.mainloop()
        
    def algorithm(self):
        rc2_list = self.data[2]
        answer = self.calc.algorithm(rc2_list)
        
        """Main box"""
        self.window.withdraw()
        window2 = Toplevel(self.window)
        window2.geometry("%dx%d" % (self.sizex, self.sizey))
        
        """Main Container"""
        c = Frame(window2, bg="white", borderwidth=1, relief="solid").grid(row=0, column=0)
    
        """Left container"""
        c_m = Frame(c, bg="white", borderwidth=1, relief="solid").grid(row=0, column=0, sticky=N+S+W+E)
        self.update_table2(c_m, self.data, self.titles)

        """Right container"""
        #c_r = tk.Frame(c, bg="white", borderwidth=1, relief="solid").grid(row=0, column=1, sticky=E)
        
        #window2.mainloop()
        
        print(answer)
   
    def load_graph(self):
        temp = self.input.get()
        if len(temp) > 0:
            self.filename = temp
            self.points = self.read_graph(self.filename)
            self.data = self.calc.calculate_all(self.points)
            self.update_table()
            self.update_graphs(self.box_mid, self.data, self.titles_tabs)
        else:
            print('niks ingevuld')
            
    def update_graphs(self, root, data, titles):
        #Connect to root
        tab_control = ttk.Notebook(root)
        """Graphs (tabs)"""
        for i in range(len(titles)):
            #Create tab
            tab = ttk.Frame(tab_control, borderwidth=1, relief="raised")
                 
            self.plot(tab, data[i], titles[i])

            #add tab
            tab_control.add(tab, text=titles[i])    
        tab_control.grid()  # grid to make visible
        
    def plot(self, root, data, title):
        fig = Figure(figsize=(6,6))
        a = fig.add_subplot(111)
       
        if data:
            temp = data
            temp2 = np.array(list(zip(*temp)))
            
            x = temp2[0]
            y = temp2[1]
        else:
            x = []
            y = []

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
    
    def update_table2(self, root, data, titles):   

        #table = Example(root)
        #table.grid()
       # scrollbar.grid_forget()

        scrollbar = Frame(root).grid()
        
        """
                root = self.table
        canvas = tk.Canvas(root, borderwidth=0, background="#ffffff")
        frame = tk.Frame(canvas, background="#ffffff")
        vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        
        vsb.grid(row=0, column=0, sticky=N+E+S)
        canvas.grid(row=0, column=0, sticky=N+S+W)
        canvas.create_window((4,4), window=frame, anchor="nw")
        
        def onFrameConfigure(canvas):
            '''Reset the scroll region to encompass the inner frame'''
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
        
        scrollbar = frame
        """
        if data:
            table_h = len(data[0])
            table_w = len(data)
            print('in data')
        else:
            return
        
        #Sets up title row
        for i in range(table_w):
            b = Label(scrollbar, text=titles[i], bg='medium spring green')
            b.grid(row=0, column=i, sticky=W+E+N+S)
           # table_conten[i].append(b)
        
        #Sets up title column (index)
        for i in range(table_h):
            text1 = 'i = ' + str(i)
            b = Label(scrollbar, text=text1, bg='white')
            b.grid(row=i+1, column=0, sticky=W+E+N+S)
            #table_conten[0].append(b)
          
        #creates rows for X coord
        for i in range(table_h):
            x = round(data[0][i][0], 3)
            b = Label(scrollbar, text=x, bg='white', borderwidth=1, relief="sunken")
            b.grid(row=i+1, column=1, sticky=W+E+N+S)
            
        #Creates rows for Y, RC1, RC2, surfaces
        for i in range(len(data)):            
            height = len(data[i])

            if i == len(data) - 1:
                for j in range(height): #Rows
                    y0 = str(round(data[i][j][0], 2))
                    y1 = str(round(data[i][j][1], 2))
                    y2 = str(round(data[i][j][2], 2))
                    b = Label(scrollbar, text=y0 + ' || ' + y1 + ' || ' + y2, bg='white', borderwidth=1, relief="sunken")
                    b.grid(row=j+1, column=i+2, sticky=W+E+N+S)
                continue
                      
            for j in range(height): #Rows
                y = round(data[i][j][1], 3)
                b = Label(scrollbar, text=y, bg='white', borderwidth=1, relief="sunken")
                b.grid(row=j+1, column=i+2, sticky=W+E+N+S)
    
    def update_table(self):         
        self.table.grid_forget()
        self.table.destroy()
        self.table = Frame(self.window, bg="white", borderwidth=1, relief="solid")
        self.table.grid(row = 0, column = 1)
       # scrollbar.grid_forget()

        root = self.table
        canvas = Canvas(root, borderwidth=0, background="#ffffff")
        frame = Frame(canvas, background="#ffffff")
        vsb = Scrollbar(root, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        
        vsb.grid(row=0, column=0, sticky=N+E+S)
        canvas.grid(row=0, column=0, sticky=N+S+W)
        canvas.create_window((4,4), window=frame, anchor="nw")
        
        def onFrameConfigure(canvas):
            '''Reset the scroll region to encompass the inner frame'''
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
        
        scrollbar = frame
        
        self.table_h = len(self.data[0])
        #Sets up title row
        for i in range(self.table_w):
            b = Label(scrollbar, text=self.titles[i], bg='medium spring green')
            b.grid(row=0, column=i, sticky=W+E+N+S)
           # table_conten[i].append(b)
        
        #Sets up title column (index)
        for i in range(self.table_h):
            text1 = 'i = ' + str(i)
            b = Label(scrollbar, text=text1, bg='white')
            b.grid(row=i+1, column=0, sticky=W+E+N+S)
            #table_conten[0].append(b)
          
        #creates rows for X coord
        for i in range(self.table_h):
            x = round(self.data[0][i][0], 3)
            b = Label(scrollbar, text=x, bg='white', borderwidth=1, relief="sunken")
            b.grid(row=i+1, column=1, sticky=W+E+N+S)
            
        #Creates rows for Y, RC1, RC2, surfaces
        for i in range(len(self.data)):            
            height = len(self.data[i])

            if i == len(self.data) - 1:
                for j in range(height): #Rows
                    y0 = str(round(self.data[i][j][0], 2))
                    y1 = str(round(self.data[i][j][1], 2))
                    y2 = str(round(self.data[i][j][2], 2))
                    b = Label(scrollbar, text=y0 + ' || ' + y1 + ' || ' + y2, bg='white', borderwidth=1, relief="sunken")
                    b.grid(row=j+1, column=i+2, sticky=W+E+N+S)
                continue
                      
            for j in range(height): #Rows
                y = round(self.data[i][j][1], 3)
                b = Label(scrollbar, text=y, bg='white', borderwidth=1, relief="sunken")
                b.grid(row=j+1, column=i+2, sticky=W+E+N+S)
      
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
        
    def calc_all(self, table, tabs):               
        self.update_table(table)
        self.update_tabs(tabs)
    

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
 