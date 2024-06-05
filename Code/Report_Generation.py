# -*- coding: utf-8 -*-
"""
Created on Fri May 31 16:17:20 2024

@author: ferbe
"""
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 21:50:48 2024

@author: ferbe
"""
class Report_Generation:
    def __init__(self):        
        self.vessels_name_Rdominance = [['LCA'],
                                        ['p-LAD','m-LAD','d-LAD'],
                                        ['D1','D2'],
                                        ['p-Cx','d-Cx'],
                                        ['OM1','OM2'],
                                        ['RI'],
                                        ['p-RCA','m-RCA','d-RCA'],
                                        ['RPD'],
                                        ['RPL']
                                        ]
        self.vessels_name_Ldominance = [['LCA'],
                                        ['p-LAD','m-LAD','d-LAD'],
                                        ['D1','D2'],
                                        ['p-Cx','d-Cx'],
                                        ['OM1','OM2'],
                                        ['LPD'],
                                        ['LPL'],
                                        ['RI'],
                                        ['p-RCA','m-RCA','d-RCA']
                                        ]
        self.vessels_name_codominance = [['LCA'],
                                        ['p-LAD','m-LAD','d-LAD'],
                                        ['D1','D2'],
                                        ['p-Cx','d-Cx'],
                                        ['OM1','OM2'],
                                        ['LPD'],
                                        ['LPL'],
                                        ['RI'],
                                        ['p-RCA','m-RCA','d-RCA'],
                                        ['RPD'],
                                        ['RPL']
                                        ]
        
        self.one_segment_tree = {'LCA':'\n·Main left coronary artery (LCA)',
                                 'RI':'\n·Ramus intermedius (RI)',
                                'RPD':'\n      -Right posterior descending artery (RPD)',
                                'RPL':'\n      -Right posterolateral artery (RPL)',
                                'LPD':'\n      -Left posterior descending artery (LPD)',
                                'LPL':'\n      -Left posterolateral artery (LPL)'
                                }        
        self.two_segments_tree = {'p-Cx':'\n·Circumflex artery (Cx)'
                                  }
        self.three_segments_tree = {'p-LAD':'\n·Left anterior descending artery (LAD)',
                                    'p-RCA':'\n·Right coronary artery (RCA)'
                                    }
                
        self.stenosis_reported = [['0','1-24','25-49','50-69','70-99','100','ND'],
                                  ['no lesions','minimal stenosis','mild stenosis','moderate stenosis','severe stenosis','a total occlusion','a non-evaluable vessel']
                                  ]
        
        self.calcium_ranges = ['0 Non-identified','1-10 Minimal','11-100 Mild','101-400 Moderate','>400 Severe']
        
  
    def final_reporting(self,data,identifier):
        var = 0 #counter for affected vessels
        report = []
        report.append(f'REPORT OF THE CORONARY ANATOMY STUDY VIA CCTA OF PATIENT {identifier}:\n')
        
        #indicate dominance
        dominance = data[identifier]['Dominance']
        report.append(f'\nCORONARY DOMINANCE: {dominance}.\n')
        
        report.append('\nDETAILED FINDINGS:')
        
        #Reporting depending on the type of dominance
        if data[identifier]['Dominance'] == 'Right dominance':
            vessels_name_list = self.vessels_name_Rdominance
        elif data[identifier]['Dominance'] == 'Left dominance':
            vessels_name_list = self.vessels_name_Ldominance
        else: 
            vessels_name_list = self.vessels_name_codominance
        
        #order in which stenosis is reported in database
        order_vessels = []
        for j in data[identifier]['Stenosis']:
            order_vessels.append(data[identifier]['Stenosis'][j][1])
            if data[identifier]['Stenosis'][j][1]!='0':
                var+=1
        
        results_stenosis = {}
        for i in range(len(vessels_name_list)):
            for j in range(len(vessels_name_list[i])):
                key = vessels_name_list[i][j]
                try:
                    idx = order_vessels.index(key)
                    results_stenosis[key] = data[identifier]['Stenosis'][idx][0]
                except:
                    results_stenosis[key] = 'NA'
        
        for artery in vessels_name_list:
            if len(artery) == 1:
                self.one_segment(report,results_stenosis,artery)
            if len(artery) == 2:
                if artery[0] == 'D1' and results_stenosis['D1']!='NA':
                    result = self.stenosis_reported[1][self.stenosis_reported[0].index(results_stenosis['D1'])]
                    report.append(f'\n      -The patient presents {result} in the first diagonal')
                    if results_stenosis['D2']!='NA':
                        result2 = self.stenosis_reported[1][self.stenosis_reported[0].index(results_stenosis['D2'])]
                        report.append(f', and {result2} in the second diagonal.')
                    else:
                        report.append('.')
                elif artery[0] == 'OM1' and results_stenosis['OM1']!='NA':
                    result = self.stenosis_reported[1][self.stenosis_reported[0].index(results_stenosis['OM1'])]
                    report.append(f'\n      -The patient presents {result} in the first obtuse marginal')
                    if results_stenosis['OM2']!='NA':
                        result2 = self.stenosis_reported[1][self.stenosis_reported[0].index(results_stenosis['OM2'])]
                        report.append(f', and {result2} in the second obtuse marginal.')
                    else:
                        report.append('.')
                else:
                    self.two_segments(report,results_stenosis,artery)
            if len(artery) == 3:
                self.three_segments(report,results_stenosis,artery)
                    
        #Report non-diagnostic vessels and calcium score too high
        calcium_score = data[identifier]['CACs']
        CADRADS = data[identifier]['CADRADS']
        
        report.append('\n')
        
        report.append('\nADDITIONAL FINDINGS: ')
        if calcium_score == '>400': 
            reported_calcium = self.calcium_ranges[4]
        elif calcium_score == '101-400': 
            reported_calcium = self.calcium_ranges[3]
        elif calcium_score == '11-100':
            reported_calcium = self.calcium_ranges[2]
        elif calcium_score == '1-10':
            reported_calcium = self.calcium_ranges[1]
        else:
            reported_calcium = self.calcium_ranges[0]
        
        if calcium_score == '101-400' or calcium_score == '>400':
            report.append(f'\nATENTION! High level of arterial calcification: {reported_calcium}.\n')
        else:
            report.append('\nThere are not additional findings.\n')
            
        try:
            report.append('\nADDITIONAL COMMENTS: ')
            if data[identifier]['Additional comments'] == '':
                report.append('\nNo additional comments.\n')
            else:
                report.append('\n')
                report.append(data[identifier]['Additional comments'])
                report.append('\n')
        except:
            pass
        
        if CADRADS == 'ND':
            #Report conclusions
            report.append('\nCONCLUSIONS:')
            report.append('NON-diagnostic study\n')
        
        else:
            #Report conclusions
            report.append('\nCONCLUSIONS: ')
            if (var == 0 and calcium_score=='0'):
                report.append('\nEpicardial coronary artery tree without parietal calcification or stenotic atherosclerotic lesions: noninvasive coronary angiography apparently within normality.')
            elif (var == 0 and calcium_score!='0'):
                report.append('\nEpicardial coronary artery tree without stenotic atherosclerotic lesions. Mild/moderate/severe calcification detected.')
            elif calcium_score=='1-10':
                report.append('\nEpicardial coronary artery tree with stenotic atherosclerotic lesions but without calcification.')
            elif calcium_score=='11-100':
                report.append('\nEpicardial coronary artery tree with stenotic atherosclerotic lesions with mild calcification.')
            elif calcium_score=='101-400':
                report.append('\nEpicardial coronary artery tree with stenotic atherosclerotic lesions with moderate calcification.')
            else:
                report.append('\nEpicardial coronary artery tree with stenotic atherosclerotic lesions with severe calcification.')
            
            #Report CAD-RADS
            report.append(f'\nAccording to the current classification system for atherosclerotic disease detected by Cardio-CT the findings are compatible with a CAD-RADS: {CADRADS}')
            try:
                if data[identifier]['Plaque'] != '':
                    report.append('/')
                    report.append(data[identifier]['Plaque'])
                if data[identifier]['HRP'] !=False:
                    report.append('/')
                    report.append('HRP')
                if data[identifier]['Ischemia']!='':
                    report.append('/')
                    report.append(data[identifier]['Ischemia'])
                if data[identifier]['Stent']!=False:
                    report.append('/')
                    report.append('S')
                if data[identifier]['Graft']!=False:
                    report.append('/')
                    report.append('G')
                if data[identifier]['Exceptions']!=False:
                    report.append('/')
                    report.append('E')
            except:
                pass                    
            
            report.append('\nWith this result, appropriate measures should be taken considering the recommendations published in the expert consensus document.')
            report.append('(Reference : CAD-RADS™ 2.0 - 2022 Coronary Artery Disease – Reporting and Data System an expert consensus document of the Society of Cardiovascular Computed Tomography. Journal of Cardiovascular Computed Tomography (2022), https://doi.org/10.1016/j.jcct.2022.07.002)')
        
        return report
        
    def one_segment(self,report,results_stenosis,artery):
        #1 GROUP
        key1 = artery[0]
        if results_stenosis[key1]!='NA':
            result = self.stenosis_reported[1][self.stenosis_reported[0].index(results_stenosis[key1])]
            report.append(self.one_segment_tree[key1])
            report.append(f'presents {result}.')
    
    def two_segments(self,report,results_stenosis,artery):        
        #2 GROUPS
        key1 = artery[0]
        key2 = artery[1]
        if (results_stenosis[key1] or [key2]) != 'NA':
            report.append(self.two_segments_tree[key1])
            if results_stenosis[key1] != 'NA':
                result = self.stenosis_reported[1][self.stenosis_reported[0].index(results_stenosis[key1])]
                report.append(f'presents {result} in its proximal segment')
                if results_stenosis[key2] != 'NA':
                    result2 = self.stenosis_reported[1][self.stenosis_reported[0].index(results_stenosis[key2])]
                    report.append(f', and {result2} in its distal segment.')
                else:
                    report.append('.')
            elif results_stenosis[key2] != 'NA':
                result = self.stenosis_reported[1][self.stenosis_reported[0].index(results_stenosis[key2])]
                report.append(f'presents {result} in its distal segment.')
    
    def three_segments(self,report,results_stenosis,artery):  
        #3 GROUPS  
        key1 = artery[0]
        key2 = artery[1]
        key3 = artery[2]
        if (results_stenosis[key1] or [key2] or [key3]) != 'NA':
            report.append(self.three_segments_tree[key1])
            if results_stenosis[key1] != 'NA':
                result = self.stenosis_reported[1][self.stenosis_reported[0].index(results_stenosis[key1])]
                report.append(f'presents {result} in its proximal segment')
                if results_stenosis[key2] != 'NA':
                    result2 = self.stenosis_reported[1][self.stenosis_reported[0].index(results_stenosis[key2])]
                    report.append(f', {result2} in its medial segment')
                    if results_stenosis[key3] != 'NA':
                        result3 = self.stenosis_reported[1][self.stenosis_reported[0].index(results_stenosis[key3])]
                        report.append(f', and {result3} in its distal segment.')
                    else:
                        report.append('.')
                elif results_stenosis[key3] != 'NA':
                    result2 = self.stenosis_reported[1][self.stenosis_reported[0].index(results_stenosis[key3])]
                    report.append(f', and {result2} in its distal segment.')
                else:
                    report.append('.')
            elif results_stenosis[key2] != 'NA':
                result = self.stenosis_reported[1][self.stenosis_reported[0].index(results_stenosis[key2])]
                report.append(f'{result} in its medial segment')
                if results_stenosis[key3] != 'NA':
                    result2 = self.stenosis_reported[1][self.stenosis_reported[0].index(results_stenosis[key3])]
                    report.append(f', and {result2} in its distal segment.')
                else:
                    report.append('.')
            elif results_stenosis[key3] != 'NA':
                result = self.stenosis_reported[1][self.stenosis_reported[0].index(results_stenosis[key3])]
                report.append(f', and {result} in its distal segment.')
                
    
    