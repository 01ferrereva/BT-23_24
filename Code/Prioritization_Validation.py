# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 21:51:56 2024

@author: ferbe
"""
from tabulate import tabulate
import pandas as pd

class Prioritization_Validation:
    def __init__(self,databaseAI,databasenotAI):
        # Define the criteria for prioritization and the weight for each value
        self.criteria_weights = {'CAD-RADS': {'0': 1,'1': 2,'2': 3,'3': 4, '4A': 5, '4B': 6, '5': 7}, # CAD-RADS: the more severe, the higher the weight
                                 'CACs': {'>400 Severe': 5, '101-400 Moderate': 4, '11-100 Mild': 3, '1-10 Minimal': 2, '0 Non-identified': 1}, # CACs: the more severe, the higher the weight
                                 'PreTest': lambda x: x,  # Raw values of Pre-test CAD score
                                 # Motives of consultation: the more severe, the higher the weight
                                 'Motive of consultation': {'Suspected acute coronary syndrome (ACS)': 15,
                                                            'Chest pain/atypical symptoms in patient without known CAD': 14,
                                                            'Alteration myocardial ischemia/perfusion test': 13,
                                                            'Nonspecific ECG/Holter alteration': 12,
                                                            'Assessment of known coronary artery disease (not revascularized)': 11, 
                                                            'Assessment of revascularized coronary artery disease': 10,
                                                            'Coronary calcification study': 9,
                                                            'Screening for coronary artery disease in cardiomyopathy': 8,
                                                            'Screening for coronary artery disease in endocarditis': 7,
                                                            'Coronary artery disease screening in systemic disease': 6,
                                                            'Coronary vein study': 5,
                                                            'Coronary anomaly study': 4,
                                                            'Checkup, patient without cardiologic symptomatology or known coronary artery disease': 3,
                                                            'No information': 2,
                                                            'Other': 1},
                                 'Marked as urgent study': {True: 2, False: 1} #If marked as urgent study, assign a higher weight to indicate more priority
                                }
        self.AI = databaseAI
        self.notAI = databasenotAI
    
    def database4prioritization_creation(self):
        data4prioritization = {}
        for i in self.AI: 
            data4prioritization[i] = {}
            data4prioritization[i]['Name'] = self.AI[i]['EHR']['Name']
            data4prioritization[i]['Critical vessels over 50% stenosis'] = True if self.AI[i]['Alarm'] != [] else False
            data4prioritization[i]['CAD-RADS'] = self.AI[i]['CADRADS']
            calcium_score = self.AI[i]['CACs']
            calcium_ranges = ['0 Non-identified','1-10 Minimal','11-100 Mild','101-400 Moderate','>400 Severe']
            if calcium_score>400: 
                reported_calcium = calcium_ranges[4]
            elif calcium_score>100: 
                reported_calcium = calcium_ranges[3]
            elif calcium_score>10:
                reported_calcium = calcium_ranges[2]
            elif calcium_score>0:
                reported_calcium = calcium_ranges[1]
            else:
                reported_calcium = calcium_ranges[0]
            data4prioritization[i]['CACs'] = reported_calcium
            data4prioritization[i]['Limitations'] = self.AI[i]['Limitations']
            data4prioritization[i]['PreTest'] = self.AI[i]['Pre-test score']
            data4prioritization[i]['Motive of consultation'] = self.AI[i]['EHR']['Consult motive']
            data4prioritization[i]['Marked as urgent study'] = True if self.AI[i]['EHR']['Urgent study']=='Yes' else False
            data4prioritization[i]['Previous procedures'] = self.AI[i]['EHR']['Previous procedures']
        for i in self.notAI: 
            data4prioritization[i] = {}
            data4prioritization[i]['Name'] = self.notAI[i]['EHR']['Name']
            data4prioritization[i]['Critical vessels over 50% stenosis'] = None
            data4prioritization[i]['CAD-RADS'] = None
            data4prioritization[i]['CACs'] = None
            data4prioritization[i]['Limitations'] = self.notAI[i]['Limitations']
            data4prioritization[i]['PreTest'] = self.notAI[i]['Pre-test score']
            data4prioritization[i]['Motive of consultation'] = self.notAI[i]['EHR']['Consult motive']
            data4prioritization[i]['Marked as urgent study'] = True if self.notAI[i]['EHR']['Urgent study']=='Yes' else False
            data4prioritization[i]['Previous procedures'] = self.notAI[i]['EHR']['Previous procedures']

        cols = ['Name','Critical vessels over 50% stenosis', 'CAD-RADS', 'CACs', 'Limitations','PreTest','Motive of consultation','Marked as urgent study','Previous procedures']
        df = pd.DataFrame.from_dict(data4prioritization, orient='index', columns=cols)
        return df
    
    # Assign priority scores to each patient based on the criteria
    def calculate_priority(self,row):
        priority_values = [] # list of weights of each characteristic
        
        # PRIOR CLASSIFICATION BETWEEN THREE MAIN GROUPS: URGENT PATIENTS, HIGH PRIORITY PATIENTS, LOW PRIORITY PATIENTS

        # Urgent cases are those which have a critical vessel (RCA, LCA, Cx, LAD) with >=50% stenosis degree
        if row['Critical vessels over 50% stenosis'] == True:
            priority_values.append(4)  # Group CRITICAL
            priority_values.append(0)  # no subclassification in this group

        # Subclassification for the group LOW, MEDIUM and HIGH
        elif pd.isna(row['Critical vessels over 50% stenosis']) or row['Critical vessels over 50% stenosis'] == False:

            # Low priority patients have a known CAD-RADS (detected through AI) of 2, 1 or 0
            if pd.notna(row['CAD-RADS']) and row['CAD-RADS'] in ['0', '1', '2']:
                priority_values.append(1)  # Group LOW
                priority_values.append(0)  # no subclassification in this group
            
            elif 'Stent/ACTP' in row['Previous procedures'] or 'Coronary bypass' in row['Previous procedures']:
                priority_values.append(3)  # Group HIGH
                priority_values.append(2)  # Subgroup STENT/BYPASS
            
            elif pd.notna(row['CAD-RADS']) and row['CAD-RADS'] in ['5', '4B', '4A']:
                priority_values.append(3)  # Group HIGH
                priority_values.append(1)  # Subgroup HIGH CAD-RADS
            
            elif pd.notna(row['CAD-RADS']) and row['CAD-RADS'] in ['3']:
                priority_values.append(2)  # Group MEDIUM
                priority_values.append(2)  # Group known image info
            
            else:
                priority_values.append(2)  # Group MEDIUM
                priority_values.append(1)  # Group unknown image info

        # CLASSIFICATION OF PATIENTS OF EACH GROUP AND SUBGROUP ACCORDING TO OTHER CRITERIA        
        for criterion, weights in self.criteria_weights.items():
            # Prioritization for CACs is as follows: 
            #   - if CACs is available, the weight is defined according to the criteria.
            #   - if CACs is not available, but the patient has 'Excessive calcification' as a Limitation of acquisition, the weight is defined as the same as for maximum CACs
            #   - if CACs is not available and the patient has not 'Excessive calcification', the weight is 0 (minimum) 
            if criterion == 'CACs':
                if pd.notna(row['CACs']):
                    cacs_value = row['CACs']
                    if cacs_value in self.criteria_weights['CACs']:
                        priority_values.append(self.criteria_weights['CACs'][cacs_value])
                    else:
                        priority_values.append(0)
                elif 'Excessive coronary calcification' in row['Limitations']:
                    priority_values.append(self.criteria_weights['CACs']['>400 Severe'])
                else:
                    priority_values.append(0)

            elif criterion == 'PreTest':
                pretest_value = row.get(criterion)
                if pd.notna(pretest_value):
                    priority_values.append(weights(pretest_value))
                else:
                    priority_values.append(0) # if there is no Pre-Test score value, the weight is 0 (minimum) to get it to the bottom of the prioritization

            #elif criterion != 'Marked as urgent study':
                # DETECT URGENT CASES FROM THE EMERGENCY ROOM
                #value = row.get('Marked as urgent study')
                #priority_values.append(self.criteria_weights['Marked as urgent study'][value])
            else:                
                value = row.get(criterion)
                if pd.notna(value) and value in weights:
                    priority_values.append(weights[value])
                else:
                    priority_values.append(0) # if there is no value, the weight is 0 (minimum) to get it to the bottom of the prioritization
        return tuple(priority_values)
        
    def set_order(self):
        data = self.database4prioritization_creation()
        data['Priority'] = data.apply(self.calculate_priority, axis=1)

        # Sort the patients based on their priority scores
        sorted_patients = data.sort_values(by=['Priority','CAD-RADS','CACs','PreTest', 'Motive of consultation', 'Marked as urgent study'], ascending=[False, False, False, False, False, False])  # All criteria ordered from highest to lowest (since higher values of all these criteria indicate higher priority)

        # Display the sorted patients
        sorted_patients = sorted_patients.to_dict('index') # transform dataframe to dict
        order = []
        order2 = []
        for i in sorted_patients:
            if sorted_patients[i]['Priority'][0]==4:
                urgency = 'Critical priority'
            elif sorted_patients[i]['Priority'][0]==3:
                urgency = 'High priority'
            elif sorted_patients[i]['Priority'][0]==2:
                urgency = 'Medium priority'
            else: 
                urgency = 'Low priority'
            
            pre_proc = []
            for j in sorted_patients[i]['Previous procedures']:
                if j == 'Stent/ACTP' or j =='Coronary bypass':
                    pre_proc.append(j)
            
            lim_calc = [] # patients with excessive calcium but without detected cacs
            lim_suboptimal = [] # patients which study has to be repeated
            for j in sorted_patients[i]['Limitations']:
                if j == 'Excessive coronary calcification':
                    lim_calc.append(j)
                elif j in ['Cardiac motion artifact','Respiratory motion artifact','Reconstructive artifact','Metallic artifacts']:
                    lim_suboptimal.append(j)
            
            if sorted_patients[i]['CACs'] == None:
                if lim_calc != []:
                    calcium_score = lim_calc[0]
                else:
                    calcium_score = '-'
            else:
                calcium_score = sorted_patients[i]['CACs']
            order.append([i,
                          sorted_patients[i]['Name'],
                          urgency,
                          sorted_patients[i]['CAD-RADS'] if sorted_patients[i]['CAD-RADS']!=None else '-',
                          pre_proc if pre_proc!=[] else '-',
                          calcium_score,
                          sorted_patients[i]['PreTest'],
                          sorted_patients[i]['Motive of consultation'],
                          sorted_patients[i]['Marked as urgent study'],
                          lim_suboptimal
                         ])
        
            order2.append([i,
                           urgency,
                           sorted_patients[i]['CAD-RADS'] if sorted_patients[i]['CAD-RADS']!=None else '-',
                           pre_proc if pre_proc!=[] else '-',
                           calcium_score,
                           sorted_patients[i]['PreTest']
                          ])
        
        # print('\n---------------------------------------------------------------------------------------------------------')
        # print('\n\033[1m'+'CASE REPORT VALIDATION ORDER'+'\033[0m\n')
        # print("\nThe following list shows the order of priority in which case reports should be validated:")
        # print(tabulate(order2,headers=['Patient ID','Urgency','CADRADS','Prev. Proc.','Calcium','PreTest'])) 
        
        
        # print('\n---------------------------------------------------------------------------------------------------------')
        # print('\n\033[1m'+'CASE REPORT VALIDATION ORDER'+'\033[0m\n')
        # print("\nThe following list shows the order of priority in which case reports should be validated:")
        # print(tabulate(order,headers=['Patient ID','Urgency','CADRADS','Prev. Proc.','Calcium','PreTest','Motive of consultation','Urgency of study'])) 
        
        return order