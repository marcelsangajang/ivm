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

class Example(tk.Frame):
    def __init__(self, root):

        tk.Frame.__init__(self, root)
        self.canvas = tk.Canvas(root, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.grid(row=0, column = 0, rowspan=2, sticky=E+N+S)
        self.canvas.grid(row=0, column = 0, rowspan = 2, sticky=N+W+S)
        self.canvas.create_window((8,8), window=self.frame, anchor="nw", 
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        #self.populate()

    def populate(self, data):
        titles = ['Index', 'X', 'Y', 'RC1', 'RC2', 'Surface i to i + 1: Total || breder || smaller ']
        """Put in some fake data
        for row in range(100):
            tk.Label(self.frame, text="%s" % row, width=3, borderwidth="1", 
                     relief="solid").grid(row=row, column=0)
            t="this is the second column for row %s" %row
            tk.Label(self.frame, text=t).grid(row=row, column=1)
        """
        table_w = len(titles)
        table_h = len(data[0])
        #Sets up title row
        for i in range(table_w):
            b = Label(self.frame, text=titles[i], bg='medium spring green')
            b.grid(row=0, column=i, sticky=W+E+N+S)
           # table_conten[i].append(b)
        
        #Sets up title column (index)
        for i in range(table_h):
            text1 = 'i = ' + str(i)
            b = Label(self.frame, text=text1, bg='white')
            b.grid(row=i+1, column=0, sticky=W+E+N+S)
            #table_conten[0].append(b)
          
        #creates rows for X coord
        for i in range(table_h):
            x = round(data[0][i][0], 3)
            b = Label(self.frame, text=x, bg='white', borderwidth=1, relief="sunken")
            b.grid(row=i+1, column=1, sticky=W+E+N+S)
            
        #Creates rows for Y, RC1, RC2, surfaces
        for i in range(len(data)):       
            height = len(data[i])

            if i == len(data) - 1:
                for j in range(height): #Rows
                    y0 = str(round(data[i][j][0], 2))
                    y1 = str(round(data[i][j][1], 2))
                    y2 = str(round(data[i][j][2], 2))
                    b = Label(self.frame, text=y0 + ' || ' + y1 + ' || ' + y2, bg='white', borderwidth=1, relief="sunken")
                    b.grid(row=j+1, column=i+2, sticky=W+E+N+S)
      
                continue
                      
            for j in range(height): #Rows
                y = round(data[i][j][1], 3)
                b = Label(self.frame, text=y, bg='white', borderwidth=1, relief="sunken")
                b.grid(row=j+1, column=i+2, sticky=W+E+N+S)
  

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
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
        self.menu = Frame(self.window, bg="orchid1", borderwidth=1, relief="solid")
        self.menu.grid(row=0, column=0, sticky=N)
        
        self.menu_label = Label(self.menu, text="Choose graph", bg='medium spring green')
        self.menu_label.grid(row=0, column=0, sticky=N+E+S+W)
        #self.menu_buttons = []
        
        self.input = Entry(self.menu, text="")
        self.input.grid(row=0, column=1)
        self.input_button = Button(self.menu, text="Load graph", command=self.load_graph, bg='orchid1')
        self.input_button.grid(row = 1, columnspan = 2, sticky=N+E+S+W)
        
        """Frame for table"""
        self.table = Frame(self.window, bg="white", borderwidth=1, relief="solid")
        self.table.grid(row=0, column=1)
        self.table_content = self.create_table(self.table)
        
        """Frame for graphs (tabs where graphis are shown)"""
        self.box_mid = Frame(self.window, bg="white", borderwidth=1, relief="solid")
        self.box_mid.grid(row=0, column=2, sticky=W+E+N+S)
        self. tab_control = ttk.Notebook(self.box_mid)
        self.tabs = self.create_graphs(self.tab_control)
        
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
    def create_graphs(self, tab_control):
        """Graphs (tabs)"""
        tabs = []
        for i in range(len(self.titles_tabs)):
            tab = ttk.Frame(tab_control, borderwidth=1, relief="raised") # Create a tab 
            #################### 
         
            tabs.append(tab)
            
            fig = Figure(figsize=(6,6))
            a = fig.add_subplot(111)
            """if :
                temp = self.data[i]
                temp2 = np.array(list(zip(*temp)))
                x = temp2[0]
                y = temp2[1]
            else:"""
            x = []
            y = []

            a.plot(x, y,color='blue')
    
            a.set_title (self.titles_tabs[i], fontsize=16)
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
 
            tab_control.add(tab, text=self.titles_tabs[i])      # Add the tab
        tab_control.grid()  # Pack to make visible
    
        return tabs
    
    def update_graphs(self):
        
        
        self.tab_control.grid_forget()
        self.tab_control.destroy()
        self.tab_control = ttk.Notebook(self.box_mid)
        """Graphs (tabs)"""
        tabs = []
        for i in range(len(self.titles_tabs)):
            tab = ttk.Frame(self.tab_control, borderwidth=1, relief="raised") # Create a tab 
            #################### 
         
            tabs.append(tab)
            
            fig = Figure(figsize=(6,6))
            a = fig.add_subplot(111)
           
            temp = self.data[i]
            temp2 = np.array(list(zip(*temp)))
            x = temp2[0]
            y = temp2[1]


            a.plot(x, y,color='blue')
    
            a.set_title (self.titles_tabs[i], fontsize=16)
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
 
            self.tab_control.add(tab, text=self.titles_tabs[i])      # Add the tab
        self.tab_control.grid()  # Pack to make visible
    
        return tabs
        
        
    def load_graph(self):
        print('in load graph')
        temp = self.input.get()
        if len(temp) > 0:
            self.filename = temp
            self.points = self.read_graph(self.filename)
            self.data = self.calc.calculate_all(self.points)
            print(self.data[len(self.data) - 1])
            self.update_table()
            self.update_graphs()
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
    def create_table(self, master):
        t_content = []
        for i in range(self.table_w):
            t_content.append([])
        
        #Sets up title row
        for i in range(self.table_w):
            b = Label(master, text=self.titles[i], bg='medium spring green')
            b.grid(row=0, column=i, sticky=W+E+N+S)
            t_content[i].append(b)
        
        #Sets up title column (index)
        for i in range(self.table_h):
            text1 = 'i = ' + str(i)
            b = Label(master, text=text1, bg='white')
            b.grid(row=i+1, column=0, sticky=W+E+N+S)
            t_content[0].append(b)
            
        for i in range(self.table_w):
            for j in range(self.table_h): #Rows
                b = Label(master, text='', bg='white', borderwidth=1, relief="sunken")
                b.grid(row=j+1, column=i, sticky=W+E+N+S)
                t_content[i].append(b)
                
        return t_content
    
    def update_table(self):         
        self.table.grid_forget()
        #self.table.destroy()
        self.table = Frame(self.window, bg="white", borderwidth=1, relief="solid")
        self.table.grid(row=0, rowspan = 2, column=1, sticky=N+E+S+W)
       # scrollbar.grid_forget()
        scrollbar = Example(self.table)
        scrollbar.populate(self.data)
        scrollbar.grid(rowspan=2, sticky=N+E+S+W)
        """
        self.table_content.clear()
        self.table_content = []
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
            self.table_content.append([])
            
            height = len(self.data[i])

            if i == len(self.data) - 1:
                for j in range(height): #Rows
                    y0 = str(round(self.data[i][j][0], 2))
                    y1 = str(round(self.data[i][j][1], 2))
                    y2 = str(round(self.data[i][j][2], 2))
                    b = Label(scrollbar, text=y0 + ' || ' + y1 + ' || ' + y2, bg='white', borderwidth=1, relief="sunken")
                    b.grid(row=j+1, column=i+2, sticky=W+E+N+S)
                    self.table_content[i].append(b)
                continue
                      
            for j in range(height): #Rows
                y = round(self.data[i][j][1], 3)
                b = Label(scrollbar, text=y, bg='white', borderwidth=1, relief="sunken")
                b.grid(row=j+1, column=i+2, sticky=W+E+N+S)
                self.table_content[i].append(b)"""
      
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
 