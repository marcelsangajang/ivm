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
from scipy.interpolate import CubicSpline
import itertools

#import gui

class Calculations:
    def __init__(self):
        pass
    
#----------------------------------------------------
#---------- Decision making algorithms---------------
#----------------------------------------------------
            
   
    def concept_6(self, x, y, x_n, y_n, ip, ip_n):
        previous_index = 0
        previous_index_n = 0
        sub_functions_x = []
        sub_functions_y = []
        sub_functions_xn = []
        sub_functions_yn = []
        
        #Split the function in sub functions around the inflection points
        for i in range(len(ip)):
            current_index = ip[i][2]
            current_index_n = ip_n[i][2]
            
            sub_functions_x.append(x[previous_index:current_index])
            sub_functions_xn.append(x_n[previous_index_n:current_index_n])
            
            sub_functions_y.append(y[previous_index:current_index])
            sub_functions_yn.append(y_n[previous_index_n:current_index_n])
            
            previous_index = current_index
            previous_index_n = current_index_n
            
        #add last sub function      
        sub_functions_x.append(x[current_index:])
        sub_functions_xn.append(x_n[current_index_n:])
        sub_functions_y.append(y[current_index:])
        sub_functions_yn.append(y_n[current_index_n:])
        
        drawing = []
        norm = []
        d2 = []
        n2 = []
        #translate to origin and scale to (100, 100)
        for i in range(len(sub_functions_x)):
            sub_drawing = list(zip(sub_functions_x[i], sub_functions_y[i]))
            sub_norm = list(zip(sub_functions_xn[i], sub_functions_yn[i]))
            d2.append(sub_drawing)
            n2.append(sub_norm)
            temp = self.translate_to_origin(sub_drawing)
            temp = self.scale(temp)
            drawing.append(temp)
            
            temp = self.translate_to_origin(sub_norm)
            temp = self.scale(temp)
            norm.append(temp)
            
        return drawing, norm

        print('subf length {}'.format(len(sub_functions_x)))
        for i in range(len(drawing)):
            temp = list(zip(*drawing[i]))
            plt.plot(temp[0], temp[1], 'blue', lw=3)
            plt.show()
            
            
            temp = list(zip(*norm[i]))
            plt.plot(temp[0], temp[1], 'red', lw=3)
            plt.show()
            
        
       
        
    
    #Checks position of inflection points
    def concept_5(self, x, y, rc2, x_n, y_n, rc2_n, max_difference = 20):
                #Inflection point calculations (concept 4 and 5)
        inflection_points = self.find_inflection_points(x, y, rc2)
        inflection_points_n = self.find_inflection_points(x_n, y_n, rc2_n)

        
        if len(inflection_points) == len(inflection_points_n):
            final_str = '\nConcept 5: nr of inflection points: f(v) = {} n(v), = {}\n'.format(len(inflection_points), len(inflection_points_n))
            ip_match = True
            for i in range(len(inflection_points)):
                v_difference = round(inflection_points[i][0] - inflection_points_n[i][0], 2)
                h_difference = round(inflection_points[i][1] - inflection_points_n[i][1], 2)
                final_str += 'Coords: f(v)=({}, {}), n(v)({}, {}) Deviation v={} h={}\n'.format(inflection_points[i][0], inflection_points[i][1], inflection_points_n[i][0], inflection_points_n[i][1], v_difference, h_difference)
                
                if abs(v_difference) > max_difference or abs(h_difference) > max_difference:    
                    ip_match = True
        
        else:
            ip_match = False
            final_str = '\nConcept 5: nr of inflection points does not match: f(v) = {}, n(v)= {}\n'.format(len(inflection_points), len(inflection_points_n))
            
        return final_str, inflection_points, inflection_points_n, ip_match
    
    def find_inflection_points(self, x, y, rc2):
        inflection_points = []
        
        if rc2[0] < 0:
            direction_prev = '-'
        else:
            direction_prev  = '+'

            
        for i in range(1, len(rc2)):
            if rc2[i] < 0:
                direction = '-'
            else:
                direction = '+'

                
            if direction != direction_prev:
                inflection_points.append([round(x[i], 2), round(y[i], 2), i])
                
            direction_prev = direction
            
        return inflection_points
            
        
                
        
    def compare_inflection_points(self, ip, ip_n):
        if len(ip) != len(ip_n):
            return None
        
        for i in range(len(ip)):
            v = abs(ip[i][0] - ip_n[i][0])
            h = abs(ip[i][1] - ip_n[i][1])
        
    def calculate_point_devation(self, graph, norm):
        string = ''
        
        if len(graph) != len(norm):
            string += 'ERROR: Length graph != length norm\n'
            return string, None, None, None
        
        #check if the x coords have same value
        str1 = ''
        str2 = ''
        total = 0
        for i in range(len(graph[0])):
            #if graph[0][i] != norm[0][i]:
                #str1 = 'X Values graph and norm dont match!'
                #str2 += '{} vs {} \n'.format(graph[0][i], norm[0][i])
                
            #measure distance between y values
            temp = graph[1][i] - norm[1][i]
            total += abs(temp)
                
        string += (str1 + str2)
        
        #calculate avg point deviation
        dev = total / len(graph[0])
        #for i in range(1, len(graph)):
        return string, dev, None, None
        
    def print_behaviour(self, function_behaviour, norm_behaviour, x, norm_x):
        #iterate to len - 1 because last point is END statement
        longest = max(len(function_behaviour), len(norm_behaviour)) 
   
       
        string1 = 'f(x): '
        string2 = 'norm: '
        string3 = '\n----BEHAVIOURAL DATA-----\n'
        string3 += 'formatted as:\n'
        string3 += '(i, left_x) direction (i, right_x)\n\n'
        string3 += '  F(X):  \n'
        string4 = '\n  Norm:\n'
        decision = 'CORRECT'
        for i in range(longest):
            if i < len(function_behaviour) - 1 and i < len(norm_behaviour) - 1:
                if function_behaviour[i][0] != norm_behaviour[i][0]:
                    decision = 'INCORRECT'
                    
            if i < len(function_behaviour) - 1:
                direction = function_behaviour[i][0]
                index = function_behaviour[i][1]
                index_next = function_behaviour[i+1][1]
                left_x = round(x[index], 2)
                right_x = round(x[index_next], 2)
                string3 += ' ({}, {}), {}, ({}, {})\n'.format(index, left_x, direction, index_next, right_x)
                
                if function_behaviour[i][0] == 'concave':
                    string1 += ' - '
                elif function_behaviour[i][0] == 'convex':
                    string1 += ' + '
                else:
                    string1 += ' 0 '
                    
                
            if i < len(norm_behaviour) - 1:
                direction = norm_behaviour[i][0]
                index = norm_behaviour[i][1]
                index_next = norm_behaviour[i+1][1]
                left_x = round(norm_x[index], 2)
                right_x = round(norm_x[index_next], 2)
                string4 += ' ({}, {}), {}, ({}, {})\n'.format(index, left_x, direction, index_next, right_x)
                
                if norm_behaviour[i][0] == 'concave':
                    string2 += ' - '
                elif norm_behaviour[i][0] == 'convex':
                    string2 += ' + '
                else:
                    string2 += ' 0 '

            
        if len(function_behaviour) != len(norm_behaviour):
            decision = 'INCORRECT'
            
        temp = string1 +'\n'+ string2
        temp2 = string3 + string4
     

 
        return temp #+ temp2
            

    
    #Returns list of bahaviour, each element contains: ['behaviour', left x, right x]
    """Note: When detecting a transition from negative to positive RC2, the next point is taken as start of convex area. 
    No interpolation method is used to determine exact coord, this is an estimation"""
    def find_function_behaviour(self, x_list, rc2_list, p = 0):
        richting_list = []
        
        #No straight lines, looks only at concave and convex behaviour
        if p == '0':
            #print('No straight line detection')
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
        #Simply considers an Y value that lies between -p < Y < p as a straight line
        else:
            #print('Straight line detection')
            #if -p < Y < p then point is close enough to Y=0 
            p = float(p)
            #Default p: Y = 0.05 and Y = -0.05
            if rc2_list[0] + p < 0: #Y < -p
                richting = 'concave'
            elif rc2_list[0] - p > 0: #Y > p
                richting = 'convex'
            else: #-p < Y < p
                richting = 'straight' #-p < Y < p
                
            #Add first element
            richting_list.append([richting, 0])
          
            for i in range(len(rc2_list)):
                if rc2_list[i] + p < 0: #Y < -p
                    richting = 'concave'
                elif rc2_list[i] - p > 0: #Y > p
                    richting = 'convex'
                else: #-p < Y < p
                    richting = 'straight' # -p < Y < p
                    
                #Compares direction to last known direction
                if richting == richting_list[-1][0]:
                    continue
                
                richting_list.append([richting, i])
                
        return richting_list
    
#----------------------------------------------------
#----------------------------------------------------
#----------------------------------------------------
        
    def calculate_all(self, drawing_data, norm_data, nr_points = 40):
        titles = ['f(v) (Raw data)', 'f(v) (Splined)']
        data_list = []
        data_listn = []
        feedback_list = []
        #Creates array for X and array for Y
        f1 = self.reduce_points(drawing_data, nr_points)
        f1 = list(zip(*f1))
        x = f1[0]
        y = f1[1]
        
        f2 = self.reduce_points(norm_data, nr_points)
        f2 = list(zip(*f2))
        xn = f2[0]
        yn = f2[1]
        
        
        data = x, y
        datan = xn, yn
        for i in range(len(titles)):
            feedback = ''
            #Tests for concept 1, if function is invalid all other concepts dont need to be tested
            if self.concept_1(x) == False:
                feedback += 'Concept 1: Failed. No further testing\n'
                data_list.append(data)
                data_listn.append(datan)
                feedback_list.append(feedback)
                break
                
            feedback += 'Concept 1: Succes\n'
            
            #Calculate functions for raw data
            if i == 0:
                rc1 = self.rc_list(x, y)
                rc2 = self.rc_list(x, rc1)
                
                rc1n = self.rc_list(xn, yn)
                rc2n = self.rc_list(xn, rc1n)
                
                data = x, y, rc1, rc2
                datan = xn, yn, rc1n, rc2n
                
                feedback += self.test_concepts(data, datan)
            #Calculate functions for splined f(v)
            elif i == 1:
                #drawing
                s = UnivariateSpline(x, y)
                xs = x
                ys = s(xs)
                rc1 = self.rc_list(xs, ys)
                rc2 = self.rc_list(xs, rc1) 
                data = xs, ys, rc1, rc2
                
                #norm
                sn = UnivariateSpline(xn, yn)
                xsn = xn
                ysn = sn(xn)
                rc1n = self.rc_list(xsn, ysn)
                rc2n = self.rc_list(xsn, rc1n)
                datan = xsn, ysn, rc1n, rc2n
                
                feedback += self.test_concepts(data, datan)
         
            
            data_list.append(data)
            data_listn.append(datan)
            feedback_list.append(feedback)
                



            
  
            
                
            
          
        

        
    #Spline XY, calc RC1, calc RC2
 

        

            


        

   
        """
        #Calculate RC1 and RC2
        #Spline XY, calculate RC1, spline RC1, calc RC2, spline RC2
        elif i == 4:
            s = UnivariateSpline(x, y, s = 1)
            ys = s(x)
            rc1 = self.rc_list(x, ys)
            
            xs = x[:-1]
            #print('1----length rc1 = {}, xs= {}'.format(len(rc1), len(xs)))
            s = UnivariateSpline(xs, rc1, s = 1)
            ys = s(x)
            rc1 = ys
           
            #print('2---length rc1 = {}, xs= {}'.format(len(rc1), len(xs)))
            rc2 = self.rc_list(x, ys) 
            
            #print('length rc2 = {}'.format(len(rc2)))
            xs = x[:-1]
            s = UnivariateSpline(xs, rc2, s = 1)
            ys = s(x)
            rc2 = ys
        #Spline XY, calc RC1, spline RC1, calc RC2
        elif i == 3:
            s = UnivariateSpline(x, y)
            ys = s(x)
            rc1 = self.rc_list(x, ys)
            
            xs = x[:-1]
            s = UnivariateSpline(xs, rc1)
            ys = s(x)
            rc1 = ys
            rc2 = self.rc_list(x, ys) 
            

        #Calc XY, spline RC1, calc RC2
        elif i == 2:
            rc1 = self.rc_list(x, y)  
            xs = x[:-1]
            s = UnivariateSpline(xs, rc1)
            ys = s(x)
            rc1 = ys
            rc2 = self.rc_list(x, ys) 
        else:
            print('Error in method calculate.all in Thesis.py')
            print(i)
            """
            
        #format: [total surface, total neg serface, total pos surface]
        #xs = x[:-2]
        #temp = list(zip(xs, rc2))
        #surfaces_list = self.surface_list(temp)
         
        #oordeel = self.beoordeel_grafiek(surfaces_list, surface_total[0])
            

        return data_list, data_listn, titles, feedback_list
    
#----------------------------------------------------
#--------- Graph Modification algorithms ------------
#----------------------------------------------------
        
    def test_concepts(self, data, datan):
        x, y, rc1, rc2 = data
        xn, yn, rc1n, rc2n = datan
        feedback = ''
                
        #Test concept 2
        if self.concept_2(rc1) == False:
            feedback += 'Concept 2: Failed\n'
        else:
            feedback += 'Concept 2: Succes\n'
            
        #Test concept 3
        temp = self.concept_3(x, rc2, xn, rc2n)
        if temp[0] == False:
            feedback += 'Concept 3: Failed\n'
            feedback += 'f(v): {}\n'.format(temp[1])
            feedback += 'n(v): {}\n'.format(temp[2])
        else:
            feedback += 'Concept 3: Succes\n'
            feedback += 'f(v): {}\n'.format(temp[1])
            feedback += 'n(v): {}\n'.format(temp[2])
        
        return feedback
                
        
    def concept_3(self, x, rc2, x_n, rc2_n, straight_lines = False):
  
        if straight_lines == False:
            p = 0
        else:
            p = 0.025
         
        #Get sequance of behaviour        
        function_behaviour = self.find_function_behaviour(x, rc2, p)
        norm_behaviour = self.find_function_behaviour(x_n, rc2_n, p)
        
        if len(function_behaviour) != len(norm_behaviour):
            return [False, function_behaviour, norm_behaviour]
        
        for i in range(1, len(function_behaviour)):
            if function_behaviour[i][0] != norm_behaviour[i][0]:
                return [False, function_behaviour, norm_behaviour]
            
        return [True, function_behaviour, norm_behaviour]
                
        
    def concept_1(self, x):
    #Checks for concept 1
        for i in range(len(x) - 1):
            if x[i + 1] <= x[i]:
                return False
            
        return True
            

            
        
    def concept_2(self, rc1):
        for i in range(len(rc1)):
            if rc1[i] <= 0:
                return False
            
        return True
        
    #Scale function a onto coordinates of function b
    def scale(self, a, b = None, y_scale = False):   
            
        if b == None or y_scale != False:
            x_last_b = 100   
            y_last_b = 100
            
          #  if len(b) > 1:
           #     last = len(b) - 1
            #    x_last_b = b[last][0]
             #   y_last_b = b[last][1]
           
            last = len(a) - 1
            x_last_a = a[last][0]
            y_last_a = a[last][1]
            
            scale_x = x_last_b / x_last_a 
            scale_y = y_last_b / y_last_a
         
            
            for i in range(len(a)):
                a[i][0] *= scale_x
                a[i][1] *= scale_y
                
        else:
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
                                     
        return a
            
    def translate_to_origin(self, points, concept5 = False):
        #print('\n before: \n {}'.format(points))
        if concept5 == False:
            output = []
            x0 = points[0][0]
            y0 = points[0][1]
            
            for i in range(len(points)):
                x = points[i][0] - x0
                y = points[i][1] - y0
                output.append([x, y])
                
            #print('\n after: \n {}'.format(points))
                
            return output
        
        else:
            pass
            
        
        
    def reduce_points(self, pixel_coords, nr_points):
        points = []
        #We want to spread 50 points evenly across the raw data
        #Deel de data set in 50 (pas op restwaarde) 
        jumpsize = len(pixel_coords) / nr_points
        if jumpsize < 1:
            nr_points = 40
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
    
#----------------------------------------------------
#------------  Basic calculations  ------------------
#----------------------------------------------------
    #Computes total surface found in given graph
    def surfaces(self, x, y):
        data = list(zip(x, y))
        
        total = 0
        neg = 0
        pos = 0
        
        for i in range(len(data) -1):
            temp = self.surface(data[i], data[i+1])
            
            total += temp[0]
            neg += temp[1]
            pos += temp[2]
            
        return total, neg, pos
    
    #Creates array of surface distribution
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
        #print('SURFACES = {}'.format(surfaces))
        return surfaces
    
    #Calculates surface between two points
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

    

