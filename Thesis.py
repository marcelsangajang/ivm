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
import itertools

#import gui

class Calculations:
    def __init__(self):
        pass
    
    def calculate_all(self, points, titles, nr_points):
        data_list = []
        
        #Creates array for X and array for Y
        temp1 = self.reduce_points(points, nr_points)
        temp = list(zip(*temp1))
        x = temp[0]
        y = temp[1]
        
        for i in range(len(titles)):
            
            #Calculate RC1 and RC2
            #Spline XY, calculate RC1, spline RC1, calc RC2, spline RC2
            if i == 4:
                s = UnivariateSpline(x, y, s=1)
                ys = s(x)
                rc1_list = self.rc_list(x, ys)
                
                xs = x[:-1]
                print('1----length rc1 = {}, xs= {}'.format(len(rc1_list), len(xs)))
                s = UnivariateSpline(xs, rc1_list, s=1)
                ys = s(x)
                rc1_list = ys
                print('2---length rc1 = {}, xs= {}'.format(len(rc1_list), len(xs)))
                rc2_list = self.rc_list(x, ys) 
                
                #print('length rc2 = {}'.format(len(rc2_list)))
                xs = x[:-1]
                s = UnivariateSpline(xs, rc2_list, s=1)
                ys = s(x)
                rc2_list = ys
            #Spline XY, calc RC1, spline RC1, calc RC2
            elif i == 3:
                s = UnivariateSpline(x, y, s=1)
                ys = s(x)
                rc1_list = self.rc_list(x, ys)
                
                xs = x[:-1]
                s = UnivariateSpline(xs, rc1_list, s=1)
                ys = s(x)
                rc1_list = ys
                rc2_list = self.rc_list(x, ys) 
                
            #Spline XY, calc RC1, calc RC2
            elif i == 1:
                s = UnivariateSpline(x, y, s=1)
                ys = s(x)
                y = ys
                rc1_list = self.rc_list(x, ys)
                rc2_list = self.rc_list(x, rc1_list)      
            #Calc XY, spline RC1, calc RC2
            elif i == 2:
                rc1_list = self.rc_list(x, y)  
                xs = x[:-1]
                s = UnivariateSpline(xs, rc1_list, s=1)
                ys = s(x)
                rc1_list = ys
                rc2_list = self.rc_list(x, ys) 
            elif i == 0:
                #Calculate RC1 and RC2 based on raw input data 
                rc1_list = self.rc_list(x, y)
                rc2_list = self.rc_list(x, rc1_list)
            else:
                print('Error in method calculate.all in Thesis.py')
                print(i)
                
            #format: [total surface, total neg serface, total pos surface]
            xs = x[:-2]
            temp = list(zip(xs, rc2_list))
            surfaces_list = self.surface_list(temp)
             
            #oordeel = self.beoordeel_grafiek(surfaces_list, surface_total[0])
            
            data = x, y, rc1_list, rc2_list, surfaces_list
            data_list.append(data)
        return data_list
    
    #Scale function a onto coordinates of function b
    def scale(self, a, b, y_scale = False):
        
        if y_scale == False:
            x_last_b = 100   
            if len(b) > 1:
                last = len(b) - 1
                x_last_b = b[last][0]
                
            last = len(a) - 1
            x_last_a = a[last][0]
            
            scale = x_last_b / x_last_a 
         
            
            for i in range(len(a)):
                a[i][0] *= scale
                a[i][1] *= scale
                
          
        else:
            x_last_b = 100   
            y_last_b = 100
            
            if len(b) > 1:
                last = len(b) - 1
                x_last_b = b[last][0]
                y_last_b = b[last][1]
           
            last = len(a) - 1
            x_last_a = a[last][0]
            y_last_a = a[last][1]
            
            scale_x = x_last_b / x_last_a 
            scale_y = y_last_b / y_last_a
         
            
            for i in range(len(a)):
                a[i][0] *= scale_x
                a[i][1] *= scale_y
                
        return a
            
        
        
    def translate_to_origin(self, points):
        x0 = points[0][0]
        y0 = points[0][1]
        
        for i in range(len(points)):
            points[i][0] -= x0
            points[i][1] -= y0
            
        return points
        

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
     
            oordeel1.append(neg_ratio)          
            oordeel2.append(total_ratio)
             
        return oordeel1, oordeel2
        
    def beoordeel(self, x_list, rc2_list, norm_x, norm_rc2, surface_data, surface_data_norm, p):
        #Get sequance of behaviour
        method = 'simple'
        function_behaviour = self.find_function_behaviour(x_list, rc2_list, method, p)
        norm_behaviour = self.find_function_behaviour(norm_x, norm_rc2, method, p)
        
        #Check to see if desired pattern matched exactly
        """ WHEN DOING SURFACE CALCULATIONS, DATA FROM STRAIGHT LINE HAS BEEN CUT OUT"""
        pattern_match = 0
        if len(function_behaviour) == len(norm_behaviour):
            pattern_match = 1
            #Check if the behaviour sequence is the same
            for i in range(len(function_behaviour)):
                if function_behaviour[i][0] != norm_behaviour[i][0]:
                    pattern_match = 0
                    break
        
            
        string = '--- Pattern Analysis ---\n'
        #Adds end points to the behaviour array
        function_behaviour.append(['END', len(x_list) - 1])
        norm_behaviour.append(['END', len(norm_x) - 1])
        
        #Exact pattern match
        if pattern_match == 1:
            #Pattern matches, Check to see if length of found surfaces are close enough, compare surface distributions, compare surface shapes (rc3)
            #Check inner proporions:
            #Length of subgraphs correct? => sais something about knowing when a directional change takes place in the vase, and correctly drawing it in the right part of the graph
            #Inner surface distribution correct (same proportions as norm)? => 
            #Total surface distribution close to norm? =>
            #Shape of RC2 correct? => Student recognizes when walls vase are getting smaller, is this happening increasingly or decreasingly
            #All of the above correct? perfect match
            string += 'Pattern: Perfect match, comparing lengths of subgraphs...\n'
            
            #Add index of Xcoord of last element, so last subgraph length can be computed
            l = []
            ln = []
            #Finds the length of each subgraph 
            for i in range(len(function_behaviour)):
                length = 1#function_behaviour[i+1][1] - function_behaviour[i][1]
                l.append(length)
                length_norm = 1#norm_behaviour[i+1][1] - norm_behaviour[i][1]
                ln.append(length_norm)
                
            #Decide if the lengths are close enough
            
        else:
            #Pattern doesnt match, investigate further if there is still a possible match
            string += 'Pattern: No match, analysing further...\n'
            
            
            
        concave = str(100* round(surface_data[1] / surface_data[0], 4)) #percentage of surface < 0
        convex = str(100* round(surface_data[2] / surface_data[0], 4))  #percentage of surface > 0
        norm_concave = str(100* round(surface_data_norm[1] / surface_data_norm[0], 4)) #percentage of surface < 0
        norm_convex = str(100* round(surface_data_norm[2] / surface_data_norm[0], 4))  #percentage of surface > 0
        
        difference = abs(float(concave) - float(norm_concave))
        max_difference = 10
        oordeel = string
        if difference < max_difference:
            string += "--- Surface distribution: CORRECT ---\n Graph: Concave = {}%, Convex = {}%\n Norm: Concave = {}%, Convex = {}%\n Absolute difference = {}%, limit = {}%\n".format(concave, convex, norm_concave, norm_convex, difference, max_difference)
        else:
            string += "--- Surface distribution: INCORRECT ---\n Graph: Concave = {}%, Convex = {}%\n Norm: Concave = {}%, Convex = {}%\n  Absolute difference = {}%, limit = {}%\n".format(concave, convex, norm_concave, norm_convex, difference, max_difference)
            
        oordeel = self.assemble_oordeel(string, function_behaviour, norm_behaviour, x_list, norm_x)
  
        
        return oordeel
        
    def assemble_oordeel(self, oordeel, function_behaviour, norm_behaviour, x, norm_x):
        longest = max(len(function_behaviour), len(norm_behaviour))
   
       
         
        left_x = ''
        right_x = ''
        direction = ''
        oordeel += '\n--- BEHAVIOURS F(X) and NORM ---\n'
        oordeel += "Number of behaviours: f(x) = {}, norm = {}\n".format(len(function_behaviour) -1, len(norm_behaviour) -1)
        oordeel += '\nformatted as:\n'
        oordeel += '    F(X)    -------    NORM\n'
        oordeel += '(i, left_x) direction (i, right_x)\n\n'
        
        
        #iterate to len - 1 because last point is END statement
        for i in range(longest - 1):
            if i < len(function_behaviour) -1:
                direction = function_behaviour[i][0]
                index = function_behaviour[i][1]
                index_next = function_behaviour[i+1][1]
                left_x = x[index]
                right_x = x[index_next]
                oordeel += ' ({}, {}), {}, ({}, {}) ---'.format(index, left_x, direction, index_next, right_x)
            else:
                oordeel += '       NONE             ----- '
                
            if i < len(norm_behaviour) -1:
                direction = norm_behaviour[i][0]
                index = norm_behaviour[i][1]
                index_next = norm_behaviour[i+1][1]
                left_x = norm_x[index]
                right_x = norm_x[index_next]
                oordeel += '({}, {}), {}, ({}, {})\n'.format(index, left_x, direction, index_next, right_x)
            else:
                oordeel += '          NONE              \n'
            
            
            
        oordeel += '\n\n'
        return oordeel
            

    
    #Returns list of bahaviour, each element contains: ['behaviour', left x, right x]
    """Note: When detecting a transition from negative to positive RC2, the next point is taken as start of convex area. 
    No interpolation method is used to determine exact coord, this is an estimation"""
    def find_function_behaviour(self, x_list, rc2_list, method, p):
        richting_list = []
        method = None
        #Simply considers an Y value that lies between -p < Y < p as a straight line
        if method == 'simple':
            #if -p < Y < p then point is close enough to Y=0 
            p = float(p)
            #Default p: Y = 0.05 and Y = -0.05
            if rc2_list[0] - p < 0: #Y < -p
                richting = 'concave'
            elif rc2_list[0] - p > 0: #Y > p
                richting = 'convex'
            else: #-p < Y < p
                richting = 'straight' #-p < Y < p
                
            #Add first element
            richting_list.append([richting, 0])
          
            for i in range(len(rc2_list)):
                if rc2_list[i] - p < 0: #Y < -p
                    richting = 'concave'
                elif rc2_list[i] - p > 0: #Y > p
                    richting = 'convex'
                else: #-p < Y < p
                    richting = 'straight' # -p < Y < p
                    
                #Compares direction to last known direction
                if richting == richting_list[-1][0]:
                    continue
                
                richting_list.append([richting, i])
        #No straight lines, looks only at concave and convex behaviour
        else:
            if rc2_list[0] < 0: #Y < -p
                richting = 'concave'
            else: #rc2_list[0] > 0: #Y > p
                richting = 'convex'
            
            richting_list.append([richting, 0])
            for i in range(len(rc2_list)):
                if rc2_list[i] < 0: #Y < -p
                    richting = 'concave'
                else: #rc2_list[i] > 0: #Y > p
                    richting = 'convex'
                  
                #Compares direction to last known direction
                if richting == richting_list[-1][0]:
                    continue
                
                richting_list.append([richting, i])
        
        #returns ['richting', index of Coord] 
        return richting_list
    
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

    

