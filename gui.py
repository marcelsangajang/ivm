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
from scipy.interpolate import UnivariateSpline
#https://stackoverflow.com/questions/31440167/placing-plot-on-tkinter-main-window-in-python
#https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/
#Drawing graphs https://www.python-course.eu/tkinter_events_binds.php
#https://gist.github.com/EugeneBakin/76c8f9bcec5b390e45df scrollframe
#https://stackoverflow.com/questions/17125842/changing-the-text-on-a-label
#https://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-group-of-widgets-in-tkinter/3092341#3092341
 
class Gui:
    def __init__(self, root):
        self.calc = Thesis.Calculations()
        self.filename = '1'
        self.filepath = './graphs/'
        self.file_list = ['0']

        self.raw_points = []#self.read_graph(self.filename)
        #Calculates all values
        self.raw_data = [] #Contains multiple vectors, each vector contains: [x, y, rc1, rc2] 
        self.data = [] #Contains 1 vector: [x, y, rc1, rc2], based on the raw points read from file
        self.w_canvas = 500
        self.h_canvas = 500
        self.inp = None
        self.titles_table = ['Index', 'X', 'Y', 'RC1', 'RC2']
        self.titles_tabs = ['f(x)', 'RC1', 'RC2']
        self.titles_mastertabs = ['After splining f(x) and RC1', 'After splining f(x)', 'After splining RC1']
        self.table_h = 20
        self.table_w = len(self.titles_table)
        
     
        self.ratio_table = []
        self.answer_table = []
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
        
                # Create a Tkinter variable
        self.tkvar = StringVar(self.menu1)
         
        # Dictionary with options
        self.choices = {'0'}
        
        self.tkvar.set('0') # set the default option
         
        self.popupMenu = OptionMenu(self.menu1, self.tkvar, *self.choices)
        Label(self.menu1, bg="spring green", text="Choose graph").grid(row=2, column=0, sticky=N+E+S+W)
        self.popupMenu.grid(row=2, column=1)
        
        # on change dropdown value
        def change_dropdown(*args):
            print( self.tkvar.get() )
         
        # link function to change dropdown
        self.tkvar.trace('w', change_dropdown)
        
        self.update_filelist()

        
        self.input_button = Button(self.menu1, text="Load graph", command=self.load_graph, bg='green3')
        self.input_button.grid(row = 3, columnspan = 2, sticky=N+E+S+W)
        
        self.input_button3 = Button(self.menu1, text="Draw graph", command=self.drawing, bg='mediumorchid3')
        self.input_button3.grid(row=6, columnspan = 2, sticky=W+N+S+E)
        
        
        
    def update_filelist(self):
        files = []
        tempfiles = []
        self.choices.clear()
                #Find all txt files, creates a non-taken name
        for file in os.listdir(self.filepath):
            if file.endswith(".txt"):
                temp = re.sub("\D", "", file)
                if len(temp) > 0:
                    files.append(temp)
                    tempfiles.append(int(temp))
        #Find files
        self.file_list = files
        tempfiles.sort()
   
        for i in range(len(tempfiles)):
            self.choices.update({tempfiles[i]})
            
      
        menu = self.popupMenu["menu"]
        menu.delete(0, "end")
        for string in self.choices:
            menu.add_command(label=string, 
                             command=lambda value=string: self.tkvar.set(value))
            
    def algorithm(self):
        
        #Get values from user input
        n_size = int(self.inp1.get())
        neg_limit = float(self.inp2.get())
        total_limit = float(self.inp3.get())
        
        #Perform calculations
        titles = ['Index', 'Verhouding B - S', 'Oppervlakte ratio ']
        rc2_list = self.data[len(self.data) - 1]
        
        
        
        ratios = self.calc.algorithm(self.x, rc2_list, n_size)
        answer = self.calc.assessment(ratios, neg_limit, total_limit)
    
        self.ratio_table.clear()
        self.answer_table.clear()
        self.ratio_table.append(ratios[0])
        self.ratio_table.append(ratios[1])
        self.answer_table.append(answer[0])
        self.answer_table.append(answer[1])
        #print(self.ratio_table)
        main_titles = []
        
        #Window
        w = Tk()
        w.grid()
     
        t = Frame(w, bg="white", borderwidth=1, relief="solid")
        t.grid(sticky=N+E+W+S)
        e = Example(t)
        e.grid()
        e.update_table2(self.ratio_table, self.answer_table, titles, n_size, neg_limit, total_limit)
        #self.assess(e, 5, 0.6, 0.25)
        #Buttons
        #print('----ratio table en answer table---')
        #print(self.ratio_table[0])
        #print(self.answer_table[0])
        #w.mainloop()
        #Table
      
    def load_graph(self):
        temp = self.tkvar.get()
        if len(temp) == 0:               
            print('niks ingevuld')
            return
              
        self.filename = temp
        self.raw_points = self.read_graph(self.filename) 
        self.raw_data = self.calc.calculate_all(self.raw_points)
            
        window = Tk()
        window.grid()
        window.title('Grafiek {}'.format(temp))
        
        mastertabs = ttk.Notebook(window)
  
        """Graphs (tabs)"""
        for i in range(len(self.titles_mastertabs)):
            #Create tab
            
            tab = ttk.Frame(mastertabs, borderwidth=1, relief="raised")
         
            self.data = self.raw_data[i]
            print(str(self.data[3][20]))
            self.table_h = len(self.data[i])
            
            """Add frame for table"""
            table = Frame(tab, bg="white", borderwidth=1, relief="solid")
            table.grid(row=0, column=1, sticky=N+E+W+S)
            e = Example(table)
            e.grid()
            e.update_table(self.data, self.titles_table)
      
            #Tabs and graphs
            #self.box_mid.grid_remove()
           # self.box_mid.destroy()
           
            """Add frame for graphs"""
            box_mid = Frame(tab, bg="white", borderwidth=1, relief="solid")
            box_mid.grid(row=0, column=0, sticky=W+E+N+S)
            self.x = self.raw_data[0][0]
            y_coords = self.raw_data[i][1:]
            y_coords = y_coords[:-1]
            self.update_graphs(box_mid, self.x, y_coords, self.titles_tabs)
            #add tab
            
            """Add text to mainscreen"""
            T = Text(tab)
            T.grid(row=0, column=2, sticky=N+E+S+W)
            
            decision = "CORRECT"
            
            norm = ['concave', 'convex']
            string = self.calc.beoordeel(self.data[0], self.data[3], norm)
            T.insert(END, string)
             
             
            surface_data = self.data[len(self.data)-1]
            print(surface_data)
            concave = str(100* round(surface_data[1] / surface_data[0], 4)) #percentage of surface < 0
            convex = str(100* round(surface_data[2] / surface_data[0], 4))  #percentage of surface > 0
         
            string = "--- Surface distribution: {} ---\n Graph: Concave: {}%, Convex: {}%\n Norm: Concave: {}%, Convex: {}%\n".format(decision,concave, convex, concave, convex)
            T.insert(END, string)

            #add tab
            mastertabs.add(tab, text=self.titles_mastertabs[i])    
        mastertabs.grid(sticky=N)  # grid to make visible

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
        
        def toggle(event):
        	global spline
        	if spline == 0:
        		c.itemconfigure(tag1, smooth=1)
        		spline = 1
        	elif spline == 1:
        		c.itemconfigure(tag1, smooth=0)
        		spline = 0
        	return spline
        
        c = Canvas(root, bg="white", width=self.w_canvas, height=self.h_canvas)       
        c.configure(cursor="crosshair")       
        c.grid(row=0)     
        c.bind("<B1-Motion>", point)
        c.bind("<Button-2>", toggle)
        
        def clicked2():
            #self.calc_all(table, tabs)
            c.delete("all")
            points_drawing.clear()
            
        #Stores drawing as file
        def clicked3():
            self.save_graph(points_drawing) 
            points_drawing.clear()
            self.update_filelist()
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
                
            if len(y_coords[i]) != len(x):
                x = x[:-1]
                
            self.plot(tab, x, y_coords[i], titles[i])
          
            #add tab
            tab_control.add(tab, text=titles[i])    
        tab_control.grid()  # grid to make visible
        
    def plot(self, root, x, y, title):

            
        s = UnivariateSpline(x, y, s=1)
        ys = s(x)

        fig = Figure(figsize=(6,6))
        a = fig.add_subplot(111)
       
        a.plot(x, y,color='blue')
        a.plot(x, ys, color='orange')
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
        table_w = len(titles) - 1 #+1 for index column
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
                
                
    def update_table2(self, data, answer, titles, n_size, neg_limit, total_limit):         
        scrollbar = self.frame
        table_w = len(data) #+1 for index column
        table_h = len(data[0]) #+1 for title row
        #Sets up title row
        for i in range(len(titles)):
            a = Label(scrollbar, text='N size = '+ str(n_size))
            a.grid(row=0, column=0, sticky=N+E+S+W)
            
            a = Label(scrollbar, text='B/S ratio = ' + str(neg_limit))
            a.grid(row=0, column=1, sticky=N+E+S+W)
            
            a = Label(scrollbar, text='Opp ratio = ' + str(total_limit))
            a.grid(row=0, column=2, sticky=N+E+S+W)
            
            b = Label(scrollbar, text=titles[i], bg='medium spring green')
            b.grid(row=1, column=i, sticky=W+E+N+S)
           # table_conten[i].append(b)
        
        #Sets up title column (index)
        for i in range(table_h):
            text1 = 'i = ' + str(i)
            b = Label(scrollbar, text=text1, bg='white')
            b.grid(row=i+2, column=0, sticky=W+E+N+S)
            #table_conten[0].append(b)
          
        #Creates rows for Y, RC1, RC2
        for i in range(table_w):            
            height = len(data[i])
            
            for j in range(height): #Rows
                y = round(data[i][j], 3)
                if answer[i][j] == 'r':
                    bg = 'white'
                elif answer[i][j] == 'b':
                    bg = 'orange2'
                elif answer[i][j] == 's':
                    bg = 'green2'
                else:
                    bg = 'light grey'
                
                b = Label(scrollbar, text=y, bg=bg, borderwidth=1, relief="sunken")
                b.grid(row=j+2, column=i+1, sticky=W+E+N+S)

if __name__ == '__main__':
    root = Tk()
    root.title('Control panel')
    g = Gui(root)
    root.mainloop()
 
    """ 
    def lsq(self, points):
        print('in nieuwe func')
        
        def gen_data(t, a, b, c, noise=0, n_outliers=0, random_state=0):
            y = a + b * np.exp(t * c)
        
            rnd = np.random.RandomState(random_state)
            error = noise * rnd.randn(t.size)
            outliers = rnd.randint(0, t.size, n_outliers)
            error[outliers] *= 10
        
            return y + error
        
        def fun(x, t, y):
            return x[0] + x[1] * np.exp(x[2] * t) - y

        x0 = np.array([1.0, 1.0, 0.0])
        
        temp = list(zip(*points))
        print(temp)
        t_train = np.array(temp[0])
        y_train = np.array(temp[1])
     
        res_lsq = least_squares(fun, x0, loss='cauchy', f_scale=0.1, args=(t_train, y_train))
        

       
        y_lsq = gen_data(t_test, *res_lsq.x)
        print(y_lsq)
        
        
        import matplotlib.pyplot as plt

       
        plt.plot(t_test, y_lsq, label='linear loss')
        
        plt.xlabel("t")
        plt.ylabel("y")
        plt.legend()
        plt.show()
    """