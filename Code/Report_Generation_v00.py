# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 21:50:48 2024

@author: ferbe
"""
class Report_Generation:
    def __init__(self):        
        # Name of the vessels reported depending on the type of dominance (for report generation)
        # self.vessels_name_Rdominance = [['\n·Main left coronary artery (LCA)','LCA'],
        #                                 ['      -Proximal Left anterior descending artery (p-LAD)','p-LAD'],
        #                                 ['      -Medial Left anterior descending artery (m-LAD)','m-LAD'],
        #                                 ['      -Distal Left anterior descending artery (d-LAD)','d-LAD'],
        #                                 ['         -Diagonal 1 (D1)','D1'],
        #                                 ['         -Diagonal 2 (D2)','D2'],
        #                                 ['      -Proximal Circumflex artery (p-Cx)','p-Cx'],
        #                                 #['      -Medial Circumflex artery (m-Cx)','m-Cx'],
        #                                 ['      -Distal Circumflex artery (d-Cx)','d-Cx'],
        #                                 ['         -Obtuse marginal 1 (OM1)','OM1'],
        #                                 ['         -Obtuse marginal 2 (OM2)','OM2'],
        #                                 ['\n   ·Ramus Intermedius (RI)','RI'],
        #                                 ['      -Proximal Right coronary artery (p-RCA)','p-RCA'],
        #                                 ['      -Medial Right coronary artery (m-RCA)','m-RCA'],
        #                                 ['      -Distal Right coronary artery (d-RCA)','d-RCA'],
        #                                 ['\n   ·Right posterior descending artery (RPD)','RPD'],
        #                                 ['   ·Right posterolateral artery (RPL)','RPL']
        #                                ]
        # self.vessels_name_codominance = [['\n·Main left coronary artery (LCA)','LCA'],
        #                                 ['      -Proximal Left anterior descending artery (p-LAD)','p-LAD'],
        #                                 ['      -Medial Left anterior descending artery (m-LAD)','m-LAD'],
        #                                 ['      -Distal Left anterior descending artery (d-LAD)','d-LAD'],
        #                                 ['         -Diagonal 1 (D1)','D1'],
        #                                 ['         -Diagonal 2 (D2)','D2'],
        #                                 ['      -Proximal Circumflex artery (p-Cx)','p-Cx'],
        #                                 #['      -Medial Circumflex artery (m-Cx)','m-Cx'],
        #                                 ['      -Distal Circumflex artery (d-Cx)','d-Cx'],
        #                                 ['         -Obtuse marginal 1 (OM1)','OM1'],
        #                                 ['         -Obtuse marginal 2 (OM2)','OM2'],
        #                                 ['\n      ·Left posterior descending artery (LPD)','LPD'],
        #                                 ['      ·Left posterolateral artery (LPL)','LPL'],
        #                                 ['\n   ·Ramus Intermedius (RI)','RI'],
        #                                 ['      -Proximal Right coronary artery (p-RCA)','p-RCA'],
        #                                 ['      -Medial Right coronary artery (m-RCA)','m-RCA'],
        #                                 ['      -Distal Right coronary artery (p-RCA)','d-RCA'],
        #                                 ['\n   ·Right posterior descending artery (RPD)','RPD'],
        #                                 ['   ·Right posterolateral artery (RPL)','RPL']
        #                                ]
        # self.vessels_name_Ldominance = [['\n·Main left coronary artery (LCA)','LCA'],
        #                                 ['      -Proximal Left anterior descending artery (p-LAD)','p-LAD'],
        #                                 ['      -Medial Left anterior descending artery (m-LAD)','m-LAD'],
        #                                 ['      -Distal Left anterior descending artery (d-LAD)','d-LAD'],
        #                                 ['         -Diagonal 1 (D1)','D1'],
        #                                 ['         -Diagonal 2 (D2)','D2'],
        #                                 ['      -Proximal Circumflex artery (p-Cx)','p-Cx'],
        #                                 #['      -Medial Circumflex artery (m-Cx)','m-Cx'],
        #                                 ['      -Distal Circumflex artery (d-Cx)','d-Cx'],
        #                                 ['         -Obtuse marginal 1 (OM1)','OM1'],
        #                                 ['         -Obtuse marginal 2 (OM2)','OM2'],
        #                                 ['\n      ·Left posterior descending artery (LPD)','LPD'],
        #                                 ['      ·Left posterolateral artery (LPL)','LPL'],
        #                                 ['\n   ·Ramus Intermedius (RI)','RI'],
        #                                 ['      -Proximal Right coronary artery (p-RCA)','p-RCA'],
        #                                 ['      -Medial Right coronary artery (m-RCA)','m-RCA'],
        #                                 ['      -Distal Right coronary artery (p-RCA)','d-RCA']
        #                                ]
        
        self.vessels_name_Rdominance = [['\n·Main left coronary artery (LCA)','LCA'],
                                        ['\n·Left anterior descending artery',('p-LAD','m-LAD','d-LAD')],
                                        ['         -Diagonal branches (Dx)',('D1','D2')],
                                        ['\n·Circumflex artery',('p-Cx','d-Cx')],
                                        ['         -Obtuse marginal branches (OM)',('OM1','OM2')],
                                        ['\n·Ramus Intermedius (RI)','RI'],
                                        ['\n·Right coronary artery',('p-RCA','m-RCA','d-RCA')],
                                        ['         -Right posterior descending artery (RPD)','RPD'],
                                        ['         -Right posterolateral artery (RPL)','RPL']
                                        ]
        
        
        self.stenosis_reporting = [['0','1-24','25-49','50-69','70-99','100'],
                                   ['0% No stenosis','1-24% Minimal stenosis','25-49% Mild stenosis','50-69% Moderate stenosis','70-99% Severe stenosis','100% Total occlusion']
                                  ]
        
        self.calcium_ranges = ['0 Non-identified','1-10 Minimal','11-100 Mild','101-400 Moderate','>400 Severe']
        
    # # Input according information into template report
    # def preliminary_reporting(self,data,identifier):
    #     var = 0 #counter for affected vessels
    #     print('\n\033[1m'+f'PRELIMINARY REPORT OF THE CORONARY ANATOMY STUDY VIA CCTA OF PATIENT {identifier}:'+'\033[0m')

    #     #indicate dominance
    #     dominance = data[identifier]['Dominance']
    #     print(f'Coronary dominance: {dominance}.')

    #     #Reporting depending on the type of dominance
    #     if data[identifier]['Dominance'] == 'Right dominance':
    #         vessels_name_list = self.vessels_name_Rdominance
    #     elif data[identifier]['Dominance'] == 'Left dominance':
    #         vessels_name_list = self.vessels_name_Ldominance
    #     else: 
    #         vessels_name_list = self.vessels_name_codominance
            
    #     for i in vessels_name_list:
    #         if i[1]=='D1':
    #             print('·Diagonal branch/es (Dx)') # for group of diagonal branches, put a preliminary title
    #         if i[1]=='OM1':
    #             print('·Obtuse Marginal artery/ies (OM)') # for group of marginal branches, put a preliminary title
    #         for j in data[identifier]['Stenosis']:        
    #             if data[identifier]['Stenosis'][j][1]==i[1]: # check the reporting name of the evaluated vessel           
    #                 stenosis = data[identifier]['Stenosis'][j][0]
    #                 for k in range(len(self.stenosis_reporting[0])):
    #                     if data[identifier]['Stenosis'][j][0] in self.stenosis_reporting[0][k]: # stenosis detected to reporting format
    #                         stenosis_name = self.stenosis_reporting[1][k]
    #                 if stenosis == '0':
    #                     print(f'{i[0]}: No lesions.') # if range of stenosis is 0%
    #                 else:
    #                     print(f'{i[0]}: {stenosis_name}.')                
    #                     var+=1
    #                 break
    #             elif j == sorted(data[identifier]['Stenosis'].keys())[-1]: # to indicate that x vessel is non-existent or not detected
    #                 print(f'{i[0]}: NA.')
        
    #     #Report severe vessels and calcium score too high
    #     calcium_score = data[identifier]['CACs']
    #     if calcium_score =='0':
    #         max_calcium = int(calcium_score)
    #     elif calcium_score == '>400':
    #         max_calcium = 400
    #     else:
    #         max_calcium = calcium_score[calcium_score.index('-')+1:]
    #     CADRADS = data[identifier]['CADRADS']
        
    #     if max_calcium>400: 
    #         reported_calcium = self.calcium_ranges[4]
    #     elif max_calcium>100: 
    #         reported_calcium = self.calcium_ranges[3]
    #     elif max_calcium>10:
    #         reported_calcium = self.calcium_ranges[2]
    #     elif max_calcium>0:
    #         reported_calcium = self.calcium_ranges[1]
    #     else:
    #         reported_calcium = self.calcium_ranges[0]
        
    #     print('\n-Additional findings:')
    #     if data[identifier]['Alarm'] != []:
    #         print('\033[93m'+'\nATENTION!'+'\033[0m'+'Critical vessels with a worrisome level of stenosis have been detected: ')
    #         print(*data[identifier]['Alarm'],sep=', ')
    #     if calcium_score>100:
    #         print('\033[93m'+'\nATENTION!'+'\033[0m'+f'High level of arterial calcification: {reported_calcium}.')


    #     #Report conclusions
    #     print('\nCONCLUSIONES')
    #     if (var == 0 and data[identifier]['CACs']<11):
    #         print('Epicardial coronary artery tree without parietal calcification or stenotic atherosclerotic lesions: noninvasive coronary angiography apparently within normality.')
    #     elif (var == 0 and data[identifier]['CACs']>10):
    #         print('Epicardial coronary artery tree without stenotic atherosclerotic lesions. Mild/moderate/severe calcification detected.')
    #     elif data[identifier]['CACs']<11:
    #         print('Epicardial coronary artery tree with stenotic atherosclerotic lesions but without calcification.')
    #     elif data[identifier]['CACs']<101:
    #         print('Epicardial coronary artery tree with stenotic atherosclerotic lesions with mild calcification.')
    #     elif data[identifier]['CACs']<401:
    #         print('Epicardial coronary artery tree with stenotic atherosclerotic lesions with moderate calcification.')
    #     else:
    #         print('Epicardial coronary artery tree with stenotic atherosclerotic lesions with severe calcification.')

    #     #Report CAD-RADS
    #     print(f'\nAccording to the current classification system for atherosclerotic disease detected by Cardio-CT (CAD-RADS) the findings are compatible with the level of {CADRADS} (0-5)')

    #     print('\nWith this result, appropriate measures should be taken considering the recommendations published in the expert consensus document.')
    #     print('(Reference : CAD-RADS™ 2.0 - 2022 Coronary Artery Disease – Reporting and Data System an expert consensus document of the Society of Cardiovascular Computed Tomography. Journal of Cardiovascular Computed Tomography (2022), https://doi.org/10.1016/j.jcct.2022.07.002)')
                
    def final_reporting(self,data,identifier):
        var = 0 #counter for affected vessels
        report = []
        report.append(f'REPORT OF THE CORONARY ANATOMY STUDY VIA CCTA OF PATIENT {identifier}:')
        #print('\n\033[1m'+f'PRELIMINARY REPORT OF THE CORONARY ANATOMY STUDY VIA CCTA OF PATIENT {identifier}:'+'\033[0m')

        #indicate dominance
        dominance = data[identifier]['Dominance']
        report.append(f'\nCORONARY DOMINANCE: {dominance}.')
        #print(f'Coronary dominance: {dominance}.')
        
        report.append('\nDETAILED FINDINGS:')
        
        #Reporting depending on the type of dominance
        if data[identifier]['Dominance'] == 'Right dominance':
            vessels_name_list = self.vessels_name_Rdominance
        elif data[identifier]['Dominance'] == 'Left dominance':
            vessels_name_list = self.vessels_name_Ldominance
        else: 
            vessels_name_list = self.vessels_name_codominance
        
        order_vessels = []
        for j in data[identifier]['Stenosis']:
            order_vessels.append(data[identifier]['Stenosis'][j][1])
        print('ORDER VESSEELS',order_vessels)
        
        for i in range(len(vessels_name_list)):    
            try:
                index = order_vessels.index(vessels_name_list[i][1])
                stenosis = data[identifier]['Stenosis'][index][0]
                if stenosis == '0':
                    report.append(vessels_name_list[i][0])
                    report.append('presents no lesions.')
                    print(report)
            except:
                pass
            
            result_LCA = 'no lesions'
            result_pLAD= 'no lesions'
            result_mLAD= 'minimal stenosis'
            result_dLAD = 'mild stenosis'
            ·Main left coronary artery (LCA) presents {}.
            ·Left anterior descending artery (LAD) presents {} in its proximal segment, {} in its medial segment and {} in its distal segment.
            
            
            # if vessels_name_list[i][1]== 'p-LAD':
            #     report.append('\n   ·Left anterior descending artery (LAD):')
            #     #print('\nLeft anterior descending artery (LAD):')
            # elif vessels_name_list[i][1]== 'D1':
            #     report.append('\n      ·Diagonal branches (Dx):')
            #     #print('\nDiagonal branches (Dx):')
            # elif vessels_name_list[i][1]=='p-Cx':
            #     report.append('\n   ·Circumflex artery (Cx):')
            #     #print('\nCircumflex artery (Cx):')
            # elif vessels_name_list[i][1]=='OM1':
            #     report.append('\n      ·Obtuse marginal artery/ies (OM):')
            #     #print('\nObtuse marginal artery/ies (OM):')
            # elif vessels_name_list[i][1]=='p-RCA':
            #     report.append('\n·Right coronary artery (RCA):')
            #     #print('\nRight coronary artery (RCA):')
            # for j in data[identifier]['Stenosis']:                
            #     if data[identifier]['Stenosis'][j][1] == vessels_name_list[i][1]:
            #         stenosis = data[identifier]['Stenosis'][j][0]
            #         if stenosis == 0 or stenosis == '0':
            #             report.append(f'{vessels_name_list[i][0]}: No lesions.')
            #             #print(f'{vessels_name_list[i][0]}: No lesions.')
            #         elif stenosis == 'NA':
            #             pass
            #         elif stenosis == 'ND':
            #             report.append(f'{vessels_name_list[i][0]}: Non-diagnostic study.')
            #             #print(f'{vessels_name_list[i][0]}: Non-diagnostic study.')
            #         else:
            #             report.append(f'{vessels_name_list[i][0]}: {stenosis}% stenosis degree.')
            #             #print(f'{vessels_name_list[i][0]}: {stenosis}% stenosis degree.')
            #             var+=1
                

        #Report non-diagnostic vessels and calcium score too high
        calcium_score = data[identifier]['CACs']
        CADRADS = data[identifier]['CADRADS']
        
        if CADRADS == 'ND':
            #Report conclusions
            report.append('CONCLUSIONES')
            report.append('NON-diagnostic study')
            #print('\nCONCLUSIONES')
            #print('Non-diagnostic study')
        
        else:
            report.append('\nADDITIONAL FINDINGS: ')
            #print('\n-Additional findings: ')
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
                report.append(f'ATENTION! High level of arterial calcification: {reported_calcium}.')
                #print('\033[93m'+'\nATENTION!'+'\033[0m'+f'High level of arterial calcification: {reported_calcium}.')
            else:
                report.append('NA')
                #print('NA')
                
            #report.append('\nADDITIONAL COMMENTS: ')
            #report.append(data[identifier]['Additional comments'])

            #Report conclusions
            report.append('\nCONCLUSIONS: ')
            #print('\nCONCLUSIONES')
            if (var == 0 and calcium_score=='0'):
                #print('Epicardial coronary artery tree without parietal calcification or stenotic atherosclerotic lesions: noninvasive coronary angiography apparently within normality.')
                report.append('Epicardial coronary artery tree without parietal calcification or stenotic atherosclerotic lesions: noninvasive coronary angiography apparently within normality.')
            elif (var == 0 and calcium_score!='0'):
                #print('Epicardial coronary artery tree without stenotic atherosclerotic lesions. Mild/moderate/severe calcification detected.')
                report.append('Epicardial coronary artery tree without stenotic atherosclerotic lesions. Mild/moderate/severe calcification detected.')
            elif calcium_score=='1-10':
                #print('Epicardial coronary artery tree with stenotic atherosclerotic lesions but without calcification.')
                report.append('Epicardial coronary artery tree with stenotic atherosclerotic lesions but without calcification.')
            elif calcium_score=='11-100':
                #print('Epicardial coronary artery tree with stenotic atherosclerotic lesions with mild calcification.')
                report.append('Epicardial coronary artery tree with stenotic atherosclerotic lesions with mild calcification.')
            elif calcium_score=='101-400':
                #print('Epicardial coronary artery tree with stenotic atherosclerotic lesions with moderate calcification.')
                report.append('Epicardial coronary artery tree with stenotic atherosclerotic lesions with moderate calcification.')
            else:
                #print('Epicardial coronary artery tree with stenotic atherosclerotic lesions with severe calcification.')
                report.append('Epicardial coronary artery tree with stenotic atherosclerotic lesions with severe calcification.')
            
            #Report CAD-RADS
            report.append(f'\nAccording to the current classification system for atherosclerotic disease detected by Cardio-CT (CAD-RADS) the findings are compatible with the level of {CADRADS} (0-5)')
            report.append('\nWith this result, appropriate measures should be taken considering the recommendations published in the expert consensus document.')
            report.append('(Reference : CAD-RADS™ 2.0 - 2022 Coronary Artery Disease – Reporting and Data System an expert consensus document of the Society of Cardiovascular Computed Tomography. Journal of Cardiovascular Computed Tomography (2022), https://doi.org/10.1016/j.jcct.2022.07.002)')
            
            #print(f'\nAccording to the current classification system for atherosclerotic disease detected by Cardio-CT (CAD-RADS) the findings are compatible with the level of {CADRADS} (0-5)')

            #print('\nWith this result, appropriate measures should be taken considering the recommendations published in the expert consensus document.')
            #print('(Reference : CAD-RADS™ 2.0 - 2022 Coronary Artery Disease – Reporting and Data System an expert consensus document of the Society of Cardiovascular Computed Tomography. Journal of Cardiovascular Computed Tomography (2022), https://doi.org/10.1016/j.jcct.2022.07.002)')
        #print('REPORT ',report)
        return report
    
    #generate the automatic preliminar report for patients at risk
    def show_report(self,data,identifier,final=0):
        """
        print("\nWhich report do you want to open?")
        identifier = ''
        list_identifiers = [order[x][0] for x in range(len(order))]
        list_identifiers.append('E')
        while identifier not in list_identifiers:
            identifier = input("\nPlease enter the identifier of a patient in the list above or 'E' to exit: ")
        """
        if identifier == 'E':
            pass
        else:
            if final == 0:
                print('\n---------------------------------------------------------------------------------------------------------')
                print('\n\033[1m'+'AUTOMATIC PRELIMINARY CASE REPORTS'+'\033[0m\n')
                self.preliminary_reporting(data,identifier)  
            else: 
                #print('\n---------------------------------------------------------------------------------------------------------')
                #print('\n\033[1m'+'VALIDATED FINAL CASE REPORTS'+'\033[0m\n')
                report = self.final_reporting(data,identifier)
                #print('REPORT ',report)
        return report