# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 21:42:09 2024

@author: ferbe
"""
import random
import numpy as np

class ImageInfo_Generator:
    def __init__(self):        
        #Vessels reported depending on the type of dominance 
        self.main_vessels = ['LCA', # left main coronary artery (L)
                             'p-LAD', # anterior descending artery (L)
                             'm-LAD',
                             'd-LAD',
                             'p-Cx', # Circumflex artery (L)
                             #'m-Cx',
                             'd-Cx',
                             'p-RCA', # right coronary artery (R)
                             'm-RCA',
                             'd-RCA'
                            ]
        self.diagonal_branches = ['D1','D2'] # Diagonal branches (L)
        self.marginal_vessels = ['OM1','OM2','RI'] # Obtuse marginal artery/ies (L)
        self.right_vessels = ['RPD', # right posterior descending artery (R)
                              'RPL' # right posterolateral trunk (R)
                             ]
        self.left_vessels = ['LPD', # left posterior descending artery (L)
                             'LPL', # left posterolateral branch (L)
                            ]
        
        self.stenosis_values = ['0','1-24','25-49','50-69','70-99','100'] # stenosis range values (coherent with CAD-RADS ranges)
        self.stenosis_weights = [0.11,0.64,0.2,0.03,0.015,0.005] # stenosis probability of each range (from hospital register)
        
    def random_number_skewed_towards_zero(self,scale):
        # Scale = Set the scale parameter for the exponential distribution
        # Generate a random number from the exponential distribution
        rand_num = np.random.exponential(scale)

        # Clip the result to be within the range [0, 1]
        clipped_rand_num = np.clip(rand_num, 0, 1)

        return clipped_rand_num

    # Generate synthetic dictionary with random patient identifiers (id=XXXXXX)
    def image_data_generator(self,data):
        for i in data:            
            # Assign type of dominance and therefore, the existing vessels
            dominance = random.choices(['Right dominance','Left dominance','Codominance'],weights=(0.94,0.05,0.01))[0] #real data percentages
            data[i]['Dominance'] = dominance
            
            # Assign score of coronary artery calcium 
            data[i]['CACs'] = round(1000*self.random_number_skewed_towards_zero(0.1)) #calcium score from 0 to 1000 but with mean at approx. 100
            
            data[i]['Stenosis'] = {}
            
            # Assign stenosis for each vessel depending on the type of dominance
            # Assign stenosis to main vessels: LCA, RCA, Cx, LAD
            vessel_number = 0
            for j in range(len(self.main_vessels)):
                data[i]['Stenosis'][vessel_number] = [random.choices(self.stenosis_values, weights=self.stenosis_weights)[0], self.main_vessels[j]] # assign stenosis range coherent with CAD-RADS ranges, assign label to vessel
                vessel_number+=1
            
            # Assign stenosis to diagonal vessel(s) if any
            for j in range(random.randint(0,len(self.diagonal_branches))):
                data[i]['Stenosis'][vessel_number] = [random.choices(self.stenosis_values, weights=self.stenosis_weights)[0], self.diagonal_branches[j]] 
                vessel_number+=1
            
            # Assign stenosis to marginal vessel(s) if any
            for j in range(random.randint(0,len(self.marginal_vessels))):
                data[i]['Stenosis'][vessel_number] = [random.choices(self.stenosis_values, weights=self.stenosis_weights)[0], self.marginal_vessels[j]] 
                vessel_number+=1
            
            # Assign stenosis to right-dominance-related vessels
            if data[i]['Dominance'] == 'Right dominance':
                for j in range(len(self.right_vessels)):
                    data[i]['Stenosis'][vessel_number] = [random.choices(self.stenosis_values, weights=self.stenosis_weights)[0], self.right_vessels[j]]  
                    vessel_number+=1
            
            # Assign stenosis to left-dominance-related vessels
            elif data[i]['Dominance'] == 'Left dominance':
                for j in range(len(self.left_vessels)):
                    data[i]['Stenosis'][vessel_number] = [random.choices(self.stenosis_values, weights=self.stenosis_weights)[0], self.left_vessels[j]]
                    vessel_number+=1
            
            # Assign stenosis to codominance-related vessels
            else: 
                for j in range(len(self.left_vessels)):
                    data[i]['Stenosis'][vessel_number] = [random.choices(self.stenosis_values, weights=self.stenosis_weights)[0], self.left_vessels[j]]
                    vessel_number+=1
                for j in range(len(self.right_vessels)):
                    data[i]['Stenosis'][vessel_number] = [random.choices(self.stenosis_values, weights=self.stenosis_weights)[0], self.right_vessels[j]]  
                    vessel_number+=1
        return data
    
    # Calculate CAD-RADS depending on the stenosis degree
    def CADRADS_calculator(self,data,AI=True):
        if AI: # only for patients suitable of AI-analysis
            for x in data: # for each patient of the database         
                SD = [] # stenosis degrees
                alarm = [] # list of critical vessels with 70% stenosis or more
                for i in data[x]['Stenosis']: # stenosis of each vessel of patient
                    name = data[x]['Stenosis'][i][1] # name of the vessel
                    stenosis_range = data[x]['Stenosis'][i][0] # stenosis range of vessel
                    try:
                        stenosis = int(stenosis_range) # stenosis degree
                    except:
                        stenosis = int(stenosis_range[-2:]) # max stenosis degree from range
                    SD.extend([stenosis])
                    if name=='LCA':
                        LCA_index = i # save the key of the dict of vessel stenosis where the main left coronary artery is
                    #if (name=='LCA' and stenosis>49)or(name=='p-RCA' and stenosis>49)or(name=='p-Cx' and stenosis>49)or(name=='p-LAD' and stenosis>49)or(name=='m-RCA' and stenosis>49)or(name=='m-Cx' and stenosis>49)or(name=='m-LAD' and stenosis>49):
                    if (name=='LCA' and stenosis>69)or(name=='p-RCA' and stenosis>69)or(name=='p-Cx' and stenosis>69)or(name=='p-LAD' and stenosis>69)or(name=='m-RCA' and stenosis>69)or(name=='m-LAD' and stenosis>69):   
                        alarm.append((name,stenosis)) 
                SD = sorted(SD,reverse=True) # sort the (max) stenosis from higher to lower
                
                # CADRADS calculation
                if SD[0] == 100: 
                    CADRADS = '5' # vessel totally occluded
                elif int(data[x]['Stenosis'][LCA_index][0][-2:]) > 49: # max stenosis of range over 49
                    CADRADS = '4B' # left main coronary artery over 50% stenosis
                elif SD[0] > 69:   
                    if SD[1] > 69:
                        if SD[2] > 69: 
                            CADRADS = '4B' # 3 coronary vessels over 70% stenosis
                        else: 
                            CADRADS = '4A' # 2 coronary vessels over 70% stenosis
                    else: 
                        CADRADS = '4A' # 1 coronary vessel over 70% stenosis
                elif SD[0] > 49:
                    CADRADS = '3' # x coronary vessels over 50% (LCA excluded)
                elif SD[0] > 24:
                    CADRADS = '2' # x coronary vessels over 25%
                elif SD[0] > 0:
                    CADRADS = '1' # x coronary vessels over 1%
                else: 
                    CADRADS = '0' # all coronary vessels without stenosis
                data[x]['CADRADS'] = CADRADS
                data[x]['Alarm'] = alarm
                        
        else: # patients non-suitable for AI-analysis are considered non-diagnostic (ND)
            for x in data: 
                data[x]['CADRADS'] = 'ND'
        return data
    
    def CADRADS_calculator_individual(self,data,identifier):
        SD = [] # stenosis degrees
        alarm = [] # list of critical vessels with 70% stenosis or more
        for i in data[identifier]['Stenosis']: # stenosis of each vessel of patient
            name = data[identifier]['Stenosis'][i][1] # name of the vessel
            stenosis_range = data[identifier]['Stenosis'][i][0] # stenosis range of vessel
            try:
                stenosis = int(stenosis_range) # stenosis degree
            except:
                try:
                    stenosis = int(stenosis_range[-2:]) # max stenosis degree from range
                except:
                    stenosis=stenosis_range
            SD.extend([stenosis])
            if name=='LCA':
                LCA_index = i # save the key of the dict of vessel stenosis where the main left coronary artery is
            try:
                #if (name=='LCA' and stenosis>49)or(name=='p-RCA' and stenosis>49)or(name=='p-Cx' and stenosis>49)or(name=='p-LAD' and stenosis>49)or(name=='m-RCA' and stenosis>49)or(name=='m-Cx' and stenosis>49)or(name=='m-LAD' and stenosis>49):
                if (name=='LCA' and stenosis>69)or(name=='p-RCA' and stenosis>69)or(name=='p-Cx' and stenosis>69)or(name=='p-LAD' and stenosis>69)or(name=='m-RCA' and stenosis>69)or(name=='m-LAD' and stenosis>69):
                    alarm.append((name,stenosis)) 
            except:
                pass
        if 'ND' in SD:
            CADRADS='N'
            data[identifier]['CADRADS'] = CADRADS
            data[identifier]['Alarm'] = alarm
                      
            return data,CADRADS
        SD = sorted(SD,reverse=True) # sort the (max) stenosis from higher to lower
        
        # CADRADS calculation
        if SD[0] == 100: 
            CADRADS = '5' # vessel totally occluded
        elif int(data[identifier]['Stenosis'][LCA_index][0][-2:]) > 49: # max stenosis of range over 49
            CADRADS = '4B' # left main coronary artery over 50% stenosis
        elif SD[0] > 69:   
            if SD[1] > 69:
                if SD[2] > 69: 
                    CADRADS = '4B' # 3 coronary vessels over 70% stenosis
                else: 
                    CADRADS = '4A' # 2 coronary vessels over 70% stenosis
            else: 
                CADRADS = '4A' # 1 coronary vessel over 70% stenosis
        elif SD[0] > 49:
            CADRADS = '3' # x coronary vessels over 50% (LCA excluded)
        elif SD[0] > 24:
            CADRADS = '2' # x coronary vessels over 25%
        elif SD[0] > 0:
            CADRADS = '1' # x coronary vessels over 1%
        else: 
            CADRADS = '0' # all coronary vessels without stenosis
        data[identifier]['CADRADS'] = CADRADS
        data[identifier]['Alarm'] = alarm
                  
        return data,CADRADS