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

#import gui

class Calculations:
    def __init__(self):
        pass
    
    def calculate_all(self, points):
        filename = 'graph1.txt'

        #Calculate rcs
        rc1_list = self.rc_list(points)
        rc2_list = self.rc_list(rc1_list)
        
        #calculate surface
        surfaces_list = self.surface_list(rc2_list)
         #format: [total surface, total neg serface, total pos surface]
        #oordeel = self.beoordeel_grafiek(surfaces_list, surface_total[0])
        
        #returns: X, Y, RC1, RC2
        temp = list(zip(*points))
        x = temp[0]
        y = temp[1]
        temp = list(zip(*rc1_list))
        rc1 = temp[1]
        temp = list(zip(*rc2_list))
        rc2 = temp[1]
        data = x, y, rc1, rc2
        return data

    
    def algorithm(self, x_list, rc2_list, n_size):
        
        a = list(zip(x_list, rc2_list))
        print(rc2_list)
        surfaces_list = self.surface_list(a)
        surface_totals = [sum(x) for x in zip(*surfaces_list)]  #format: [total surface, total neg serface, total pos surface]
        surface_total = surface_totals[0]
        n_size = 1
        oordeel1 = []; oordeel2 = []
        
        #itereer langs de lijst met oppervlakte
        for i in range(len(surfaces_list)):
            total = 0; neg = 0; pos = 0; counter = 2*n_size + 1
            
            #Itereer langs de neighbourhood van punt i
            for j in range(2*n_size + 1):
                x = i - n_size - j 

                if x < 0 or x > len(surfaces_list) :
                    counter -= 1
                    if counter == 0:
                        counter = 1
                    continue
                
                #print("i = {}, x = {}".format(i,x))
                
                total += surfaces_list[x][0]
                neg += surfaces_list[x][1]
                pos += surfaces_list[x][2]

            if total == 0:
                total = 1

            neg_ratio = round(neg / total, 2)
            pos_ratio = round(pos / total, 2)
            total_ratio = round(total / surface_total, 2)
            
            oordeel1.append(neg_ratio)
                
            oordeel2.append(total_ratio)
             
        return oordeel1, oordeel2
    
    def assessment(self, ratios, neg_ratio, total_ratio):
        oordeel1 = []
        oordeel2 = []
        neg = ratios[0]
        tot = ratios[1]
        
        for i in range(len(neg)):
            #Vergelijk de verhouding 
            if neg[i] > neg_ratio:
                oordeel1.append('b')
            elif 1 - neg[i] > neg_ratio:
                oordeel1.append('s')
            else:
                oordeel1.append('r')
                
            #oordeel op oppervlakte ratio t.o.v. geheel
            if tot[i] > total_ratio:
                oordeel2.append('b-s')
            else:
                oordeel2.append('r')
        
        return oordeel1, oordeel2
    
    def surface_list(self, rc2_list):
        surfaces = []
        for i in range(len(rc2_list) - 1):
            temp = self.surface(rc2_list[i], rc2_list[i+1])
     
            #total surface, negative surface, positive surface
            surfaces.append([temp[0], temp[1], temp[2]])

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
    def rc_list(self, points):
        rc_list = []
        for i in range(len(points) - 1):
            #
            rc_list.append([points[i][0] , self.rc(points[i], points[i + 1])])
            
        return rc_list
            
    #returns delta y / delta x
    def rc(self, a, b):   
        #(b_y - a_y)/(b_x - b_y)
        return (b[1]-a[1])/(b[0]-a[0])

    

