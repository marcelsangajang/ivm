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
            
    def beoordeel(self, graph, norm, p):
        x = graph[0]
        y = graph[1]
        rc1 = graph[2]
        rc2 = graph[3]
        
        x_n = norm[0]
        y_n = norm[1]
        rc1_n = norm[2]
        rc2_n = norm[3]
        
        
        #Get sequance of behaviour        
        function_behaviour = self.find_function_behaviour(x, rc2, p)
        norm_behaviour = self.find_function_behaviour(x_n, rc2_n, p)
        
        #Adds end points to the behaviour array
        function_behaviour.append(['END', len(rc2) - 1])
        norm_behaviour.append(['END', len(rc2_n) - 1])
        
        str4 = self.print_behaviour(function_behaviour, norm_behaviour, x, x_n)
        
        #Remove straight linezones
        if p != '0':
            fb = []
            nb = []
            for a in function_behaviour:
                if a[0] != '0':
                    fb.append(a)
                    
            for a in norm_behaviour:
                if a[0] != '0':
                    nb.append(a)
            
            str5 = self.print_behaviour(fb, nb, x, x_n)
            function_behaviour = fb
            norm_behaviour = nb
        #Check to see if desired pattern matched exactly
        """ WHEN DOING SURFACE CALCULATIONS, DATA FROM STRAIGHT LINE HAS BEEN CUT OUT"""
        pattern_match = 1
        reasons = {
                'number_of_behaviours' : True,
                'direction_of_behaviours' : False,
                'nr_txt' : '',
                'dir_txt' : ''
                }
        

        decision = 'TRUE'
        oordeel = ''
     
        for i in range(len(x) - 1):
            if x[i + 1] <= x[i]:
                decision = 'FALSE'
                break
            
        
        oordeel += 'Step 1: {} \n'.format(decision)
        decision = 'TRUE'
        for i in range(len(y) - 1):
            if y[i+1] <= y[i]:
                decision = 'FALSE'
                break
            
        oordeel += 'Step 2: {} \n'.format(decision)
        
        #if decision == 'INCORRECT':
            #strx = '\n--- STEP 1 FAILED ---\n'
            #strx += '  A: Student does not understand the problem at all (If deviation is big)\n'
            #strx += '  B: Student understands problem, made minor mistake (If deviation is small\n'
            #strx += '  Fix B by curve fitting, then repeat step 1\n'
            #strx += '  If still incorrect -> A'
           # strx += '  Redraw the graph for further analysis\n'
            #oordeel += strx
            #return oordeel
       # else:
            #oordeel += '\n--- Step 1: SUCCES ---\n'
        
        str1 = ' '
        #str1 += '\nLevel 1.2\n'
        
        #Numbers of behaviours do not match
        if len(function_behaviour) == len(norm_behaviour):
            decision = 'CORRECT'
            #str1 += '1.1) Number of behaviours: {} (f(x)={}, norm={})\n'.format(decision, len(function_behaviour)-1, len(norm_behaviour)-1)
            #str1 += ' -Student understands that depending on the shape of the vase, \n  the water surface speed will vary.\n -Student draws correct number of speed transitions according to vase\n'
        else:
            pattern_match = 0
            reasons['number_of_behaviours'] = False
            decision = 'INCORRECT'
            #str1 += '1.1) Number of behaviours: {} (f(x)={}, norm={})\n'.format(decision, len(function_behaviour), len(norm_behaviour))
            
            #str1+= '  This can mean one of three things:\n'
            #str1 += '  A: The drawing is sloppy but could be sort of correct\n'
            #str1 += '  B: The drawing contains straight lines rather than curves\n'
            #str1 += '  C: The drawing is incorrect\n'
            #reasons['nr_txt'] += str1
            
        str2 = ''
        
        #Check if the behaviour sequence is the same
        for i in range(len(function_behaviour)):
            if function_behaviour[i][0] != norm_behaviour[i][0]:
                pattern_match = 0
                break
           
        
        if pattern_match == 1:
            str2 += 'Step 3: TRUE\n'
            reasons['direction_of_behaviours'] = True
            str2 += str4 + '\n'
            #str2 += '  Student DOES understand that:\n'
        else:
            str2 += 'Step 3: FALSE\n'
            str2 += str4 + '\n'
            #str2 += '  Student does NOT understand that:\n'
            
        

       # str2+= ' -Vase gets wider, speed at which surface rises slows down continiously,\n  resulting in a concave drawing\n'
       # str2+= ' -Vase gets smaller, speed at which surface rises slows down continiously,\n  resulting in a convex drawing\n'
        #str2+= ' -Vase width doesnt change, speed at which surface rises is constant,\n  resulting in a straight line in the drawing\n'
        reasons['dir_txt'] += str2

                
        final_str = str2

        
        #stra = '\nStep 3\n'
        #stra += 'Deviation '
        #strb = '\nStep 4\n'
        #final_str += stra + strb
        #if reasons['number_of_behaviours'] == False:
            
            #str2 += '\n--- Step 2: FAILED ---\n'
            
            
            #str2 += '  Test A, if A fails, Test B, if B fails -> C is True \n'
            
            #if p == '0':
            #    str2 += '  -Test A: press "dectecting straight lines" checkbox, select proper p value,\n  then repeat this step. If A still fails, test B\n'
            #else:
            #    str2 += '  -A tested with p = {}, still incorrect, test for B'
            #    str2 += '  -Test B: To be determined\n'
        #elif reasons['direction_of_behaviours'] == False:
            
        #else:
            #str2 += '\n--- Step 2: SUCCES ---\n'
            
        
    
        #----STEP 3 -----
        
        #Exact pattern match
        if pattern_match == 1:
            #Pattern matches, Check to see if length of found surfaces are close enough, compare surface distributions, compare surface shapes (rc3)
            #Check inner proporions:
            #Length of subgraphs correct? => sais something about knowing when a directional change takes place in the vase, and correctly drawing it in the right part of the graph
            #Inner surface distribution correct (same proportions as norm)? => 
            #Total surface distribution close to norm? =>
            #Shape of RC2 correct? => Student recognizes when walls vase are getting smaller, is this happening increasingly or decreasingly
            #All of the above correct? perfect match
            #string += 'Pattern: Perfect match, comparing lengths of subgraphs...\n'
            
            #Add index of Xcoord of last element, so last subgraph length can be computed
            st = 'Properties of type of behaviour:\n'
            #st_n = 'Norm:\n'
            st += '  Lengths:\n'
            #st_n += '  Function behaviour:\n'
            l = []
            ln = []
            answers = []
            answer_total = 0
            

            
            #Finds the length of each subgraph 
            """
            for i in range(len(function_behaviour) - 1):
                behaviour = function_behaviour[i][0]
                if behaviour == 'concave':
                    behaviour = '-'
                elif behaviour == 'convex':
                    behaviour = '+'
                else:
                    behaviour = '0'
                    
                index_next = function_behaviour[i+1][1] 
                index = function_behaviour[i][1]
                length = x[index_next] - x[index]
                #st += '    {} ({},{})\n'.format(behaviour, round(x[index_next], 2), round(y[index_next], 2))
                
                l.append(length)
                
                behaviour = norm_behaviour[i][0]
                if behaviour == 'concave':
                    behaviour = '-'
                elif behaviour == 'convex':
                    behaviour = '+'
                else:
                    behaviour = '0'
                index_next = norm_behaviour[i+1][1] 
                index = norm_behaviour[i][1]
                length_norm = x_n[index_next] - x_n[index]
                dev = None
                st += '    {}, {} vs {}, ({}%)\n'.format(behaviour, round(length, 2), round(length_norm, 2), dev)
               # st_n += '    {} ({},{})\n'.format(behaviour, round(norm_x[index_next], 4), round(y[index_next], 4))
                #st_n += '    {}, length = {}, x = {} to {}, i = {} to {}\n'.format(behaviour, round(length_norm, 2), round(x_n[index], 2), round(x_n[index_next], 2), index, index_next)
                ln.append(length_norm)
                
                answer = length / length_norm
                answer = abs(answer - 1.0)
                answers.append(answer)
                answer_total += answer
                
            #Decide if the lengths are close enough
            avg_deviation = round(100*answer_total / (len(function_behaviour) - 1), 2)
            
            str2 += st
            #str2 += st_n
            
            str2 += '\nComparison:\n'
            str2 += '  Behaviour lenghts\n'
            str2 += '    avg deviation = {}%\n'.format(avg_deviation)
            """
            
        st = '\n--- DATA --- \n'
        st_n = '\n'
         
        #graph surfaces
        #st += '  Surface graph:\n'
        #st_n += '  Surface norm:\n'
        
        #F(X) surface
        surface1 = self.surfaces(x, y)      
        total = round(surface1[0], 2)
        neg = round(surface1[1], 2)
        pos = round(surface1[2], 2) 
        #st += '    f(x): total = {}, negative = {}, positive = {}\n'.format(total, neg, pos)
        
        #RC1 surface
        surface2 = self.surfaces(x, rc1)      
        total = round(surface2[0], 2)
        neg = round(surface2[1], 2)
        pos = round(surface2[2], 2)
        #st += '    RC1: total = {}, negative = {}, positive = {}\n'.format(total, neg, pos)

        #RC2 surface
        surface3 = self.surfaces(x, rc2)      
        total = round(surface3[0], 2)
        neg = round(surface3[1], 2)
        pos = round(surface3[2], 2)
        #st += '    RC2: total = {}, negative = {}, positive = {}\n'.format(total, neg, pos)
        
        #norm surfaces
        #F(X) surface
        surface1n = self.surfaces(x_n, y_n)      
        total = round(surface1n[0], 2)
        neg = round(surface1n[1], 2)
        pos = round(surface1n[2], 2) 
        #st_n += '    f(x): total = {}, negative = {}, positive = {}\n'.format(total, neg, pos)
        
        #RC1 surface
        surface2n = self.surfaces(x_n, rc1_n)      
        total = round(surface2n[0], 2)
        neg = round(surface2n[1], 2)
        pos = round(surface2n[2], 2)
        #st_n += '    RC1: total = {}, negative = {}, positive = {}\n'.format(total, neg, pos)

        #RC2 surface
        surface3n = self.surfaces(x_n, rc2_n)      
        total = round(surface3n[0], 2)
        neg = round(surface3n[1], 2)
        pos = round(surface3n[2], 2)
        #st_n += '    RC2: total = {}, negative = {}, positive = {}\n'.format(total, neg, pos)
        
        
        str2 += st
        str2 += st_n
        str2 += '  Surface comparison:\n'
        str2 += '    f(x): graph - norm => {} - {} = {}\n'.format(round(surface1[0], 2), round(surface1n[0], 2), round(surface1[0] - surface1n[0], 2))
        str2 += '    RC1: graph - norm => {} - {} = {}\n'.format(round(surface2[0], 2), round(surface2n[0], 2), round(surface2[0] - surface2n[0], 2))
        str2 += '    RC2: graph - norm => {} - {} = {}\n'.format(round(surface3[0], 2), round(surface3n[0], 2), round(surface3[0] - surface3n[0], 2))
            
        dev = self.calculate_point_devation(graph, norm)
        
        str2 += '  Avg point deviation:\n'
        str2 += '    f(x): {}\n'.format(dev[1])
        str2 += '    RC1: {}\n'.format(dev[2])
        str2 += '    RC2: {}\n'.format(dev[3])
        
        str2+= dev[0]
            
#        concave = str(100* round(surface_data[1] / surface_data[0], 4)) #percentage of surface < 0
 #       convex = str(100* round(surface_data[2] / surface_data[0], 4))  #percentage of surface > 0
  #      norm_concave = str(100* round(surface_data_norm[1] / surface_data_norm[0], 4)) #percentage of surface < 0
   #     norm_convex = str(100* round(surface_data_norm[2] / surface_data_norm[0], 4))  #percentage of surface > 0
        
    #    difference = abs(float(concave) - float(norm_concave))
     #   max_difference = 10
       # oordeel = string
       # if difference < max_difference:
       #     string += "--- Surface distribution: CORRECT ---\n Graph: Concave = {}%, Convex = {}%\n Norm: Concave = {}%, Convex = {}%\n Absolute difference = {}%, limit = {}%\n".format(concave, convex, norm_concave, norm_convex, difference, max_difference)
      #  else:
      #      string += "--- Surface distribution: INCORRECT ---\n Graph: Concave = {}%, Convex = {}%\n Norm: Concave = {}%, Convex = {}%\n  Absolute difference = {}%, limit = {}%\n".format(concave, convex, norm_concave, norm_convex, difference, max_difference)
            
        
        #oordeel += str1 + str2
        
        #Tcreate sub functions
        

        
        oordeel += str1 + final_str 
        return oordeel
    
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
    def find_function_behaviour(self, x_list, rc2_list, p):
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
        
    def calculate_all(self, points, titles, nr_points):
        data_list = []
        
        #Creates array for X and array for Y
        temp1 = self.reduce_points(points, nr_points)
        temp = list(zip(*temp1))
  
        x = temp[0]
        y = temp[1]
        
        #Checks for concept 1
        decision = 'TRUE'
        for i in range(len(x) - 1):
            if x[i + 1] <= x[i]:
                decision = 'FALSE'
                break
            
        if decision == 'FALSE':
            plt.plot(x, y, label='data', color='blue')
            plt.show()
            import sys
            sys.exit(1)
        
        spline_type = 'univariate'
            
        if spline_type == 'univariate':
            for i in range(len(titles)):
                
                #Calculate RC1 and RC2
                #Spline XY, calculate RC1, spline RC1, calc RC2, spline RC2
                if i == 4:
                    s = UnivariateSpline(x, y, s = 1)
                    ys = s(x)
                    rc1_list = self.rc_list(x, ys)
                    
                    xs = x[:-1]
                    #print('1----length rc1 = {}, xs= {}'.format(len(rc1_list), len(xs)))
                    s = UnivariateSpline(xs, rc1_list, s = 1)
                    ys = s(x)
                    rc1_list = ys
                   
                    #print('2---length rc1 = {}, xs= {}'.format(len(rc1_list), len(xs)))
                    rc2_list = self.rc_list(x, ys) 
                    
                    #print('length rc2 = {}'.format(len(rc2_list)))
                    xs = x[:-1]
                    s = UnivariateSpline(xs, rc2_list, s = 1)
                    ys = s(x)
                    rc2_list = ys
                #Spline XY, calc RC1, spline RC1, calc RC2
                elif i == 3:
                    s = UnivariateSpline(x, y)
                    ys = s(x)
                    rc1_list = self.rc_list(x, ys)
                    
                    xs = x[:-1]
                    s = UnivariateSpline(xs, rc1_list)
                    ys = s(x)
                    rc1_list = ys
                    rc2_list = self.rc_list(x, ys) 
                    
                #Spline XY, calc RC1, calc RC2
                elif i == 1:
                    s = UnivariateSpline(x, y)
                    ys = s(x)
                    y = ys
                    rc1_list = self.rc_list(x, ys)
                    rc2_list = self.rc_list(x, rc1_list)      
                #Calc XY, spline RC1, calc RC2
                elif i == 2:
                    rc1_list = self.rc_list(x, y)  
                    xs = x[:-1]
                    s = UnivariateSpline(xs, rc1_list)
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
    
#----------------------------------------------------
#--------- Graph Modification algorithms ------------
#----------------------------------------------------
        
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

    

