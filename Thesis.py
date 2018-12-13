# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 21:19:36 2018

@author: Marcel

#Tkinter guide: http://effbot.org/tkinterbook/canvas.htm#Tkinter.Canvas.create_polygon-method
#Tkinter guide: https://likegeeks.com/python-gui-examples-tkinter-tutorial/#Create-your-first-GUI-application
#Tkinter docs: https://docs.python.org/3/library/tkinter.html#tkinter-life-preserver
# Drawing: http://zetcode.com/gui/tkinter/drawing/

"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import tkinter
from scipy.interpolate import UnivariateSpline

#import gui

class Calculations:
    def __init__(self):
        pass
    
    def calculate_all(self, points, titles=['After splining f(x) and RC1', 'After splining f(x)', 'After splining RC1'], nr_points = 50):
        filename = 'graph1.txt'
        data_list = []
        
        #Creates array for X and array for Y
        temp = self.reduce_points(points, nr_points)
        temp = list(zip(*temp))
        x = temp[0]
        y = temp[1]
        
        for i in range(len(titles)):
            #Calculate RC1 and RC2
            #Calculate RC1 and RC2 after splining XY, then splining RC1
            if i == 0:
                s = UnivariateSpline(x, y, s=1)
                ys = s(x)
                rc1_list = self.rc_list(x, ys)
                
                xs = x[:-1]
                s = UnivariateSpline(xs, rc1_list, s=1)
                ys = s(x)
                rc2_list = self.rc_list(x, ys) 
                
            #Calculate RC1 and RC2 after splining X Y
            elif i == 1:
                s = UnivariateSpline(x, y, s=1)
                ys = s(x)
     
                rc1_list = self.rc_list(x, ys)
                rc2_list = self.rc_list(x, rc1_list)      
            #Calculate RC2 after splining RC1
            elif i == 2:
                rc1_list = self.rc_list(x, y)  
                xs = x[:-1]
                s = UnivariateSpline(xs, rc1_list, s=1)
                ys = s(x)
                rc2_list = self.rc_list(x, ys) 
            else:
                #Calculate RC1 and RC2 based on raw input data 
                rc1_list = self.rc_list(x, y)
                rc2_list = self.rc_list(x, rc1_list)
                
            #format: [total surface, total neg serface, total pos surface]
            xs = x[:-2]
            temp = list(zip(xs, rc2_list))
            surfaces_list = self.surface_list(temp)
             
            #oordeel = self.beoordeel_grafiek(surfaces_list, surface_total[0])
            
            data = x, y, rc1_list, rc2_list, surfaces_list
            data_list.append(data)
        return data_list
    

    def reduce_points(self, pixel_coords, nr_points):
        points = []
        #We want to spread 50 points evenly across the raw data
        #Deel de data set in 50 (pas op restwaarde) 
        jumpsize = len(pixel_coords) / nr_points
        if jumpsize < 1:
            print('error: jumpsize < 1')
            return
        
        counter = 0
        for i in range(nr_points):
            index = int(counter)
    
            points.append(pixel_coords[index])
            counter += jumpsize
        #Elk nieuw punt krijgt avg y en x in die zone
        
        return points
    
    def algorithm(self, x_list, rc2_list, n_size):
        
        a = list(zip(x_list, rc2_list))
        surfaces_list = self.surface_list(a)
        #print('surfaces list----------')
        #print(surfaces_list)
        surface_totals = [sum(x) for x in zip(*surfaces_list)]  #format: [total surface, total neg serface, total pos surface]
        surface_total = surface_totals[0]
        
        oordeel1 = []; oordeel2 = []
        
        #itereer langs de lijst met oppervlakte
        for i in range(len(surfaces_list)):
            total = 0; neg = 0; pos = 0; counter = 0
            
            #Itereer langs de neighbourhood van punt i
            for j in range(2*n_size):
                x = i - n_size + j 

                if x < 0 or x > len(surfaces_list) - 1 :
                    continue
                
                #print("i = {}, x = {}".format(i,x))
                counter += 1
                total += surfaces_list[x][0]
                neg += surfaces_list[x][1]
                pos += surfaces_list[x][2]

 
            normalized_total = total/counter/surface_total
            
            if total == 0:
                total = 1
            neg_ratio = round(neg / total, 2)
            pos_ratio = round(pos / total, 2)
            total_ratio = round(normalized_total, 2)
           # print('Ratios: neg = {}, pos = {}, '.format(neg_ratio, pos_ratio))
            oordeel1.append(neg_ratio)          
            oordeel2.append(total_ratio)
             
        return oordeel1, oordeel2
        
    def beoordeel(self, x_list, rc2_list, norm):
        if rc2_list[0] < 0:
            richting = 'concave'
        else:
            richting = 'convex'
            
        richting_list = [richting]
        rx = [x_list[0]]
        ry = [rc2_list[0]]
        #Finds every surface 
        for i in range(len(rc2_list)):
            #Change in direction from wider to smaller
            if richting == 'concave':
                if rc2_list[i] >= 0:
                    richting = 'convex'
                    richting_list.append(richting)
                    rx.append(x_list[i])
                    ry.append(rc2_list[i])
            else:
                if rc2_list[i] < 0:
                    richting = 'concave'
                    richting_list.append(richting)
                    rx.append(x_list[i])
                    ry.append(rc2_list[i])
             

        if len(norm) != len(richting_list):
            string = "--- Structure: INCORRECT ---\n We found {}\n norm = {}\n".format(richting_list, norm)
            return string
            
        string = "--- Structure: CORRECT ---\n We found {}\n norm = {}\n".format(richting_list, norm)
        for i in range(len(richting_list)):
            if richting_list[i] != norm[i]:
                string = "--- Structure: INCORRECT ---\n We found {}\n norm = {}\n".format(richting_list, norm)
                break
            
        return string
    
    def surface_list(self, rc2_list):
        total = 0
        neg = 0
        pos = 0
        
        for i in range(len(rc2_list) - 1):
            temp = self.surface(rc2_list[i], rc2_list[i+1])
     
            #total surface, negative surface, positive surface
            #surfaces.append([temp[0], temp[1], temp[2]])
            total += temp[0]
            neg += temp[1]
            pos += temp[2]

        surfaces = [total, neg, pos]
        return surfaces
    
    def surface(self, a, b):    
        a_x = a[0]; a_y = a[1]; b_x = b[0]; b_y = b[1]
        
        if (a_y <= 0 and b_y <= 0) or (a_y >= 0 and b_y >= 0): #both y values negative or positive
            opp_vierkant = (b_x - a_x) * min(abs(a_y), abs(b_y)) #opp vierkant
            opp_driehoek = (b_x - a_x) * (max(abs(a_y), abs(b_y)) - min(abs(a_y), abs(b_y))) * 0.5
            opp = opp_vierkant + opp_driehoek
            
            if a_y <= 0:
                return opp, opp, 0
            else:
                return opp, 0, opp

        else:
            b_e = b_x - a_x
            a_d = abs(a_y) + abs(b_y)
            temp_b = b_e * (abs(a_y)/a_d)
            temp_e = b_e * (abs(b_y)/a_d)
            opp1 = 0.5*abs(a_y)*temp_b
            opp2 = 0.5*abs(b_y)*temp_e
            #b = (b + e) * (a / (a + d))
            if a_y < 0:
                return opp1 + opp2, opp1, opp2
            else:
                return opp1 + opp2, opp2, opp1
    
    #Given a list of coordinates, calculates rc for each point
    def rc_list(self, x, y):
        rc_list = []
        for i in range(len(y) - 1):
            rc = self.rc([x[i], y[i]], [x[i+1], y[i+1]])
            rc_list.append(rc)
            
        return rc_list
            
    #returns delta y / delta x
    def rc(self, a, b):   
        #(b_y - a_y)/(b_x - b_y)
        return (b[1]-a[1])/(b[0]-a[0])

    

