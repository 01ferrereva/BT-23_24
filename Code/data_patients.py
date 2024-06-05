# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 14:32:46 2024

@author: ferbel
"""
from datetime import datetime

from ImageInfo_Generator import ImageInfo_Generator
from PreTestScore import PreTestScore

class data_patients():
    def __init__(self):
        self.patients={}
        self.patients['238295']={}
        self.patients['238295']['EHR']={}
        self.patients['238295']['EHR']['Consult motive']='Chest pain/atypical symptoms in patient without known CAD'
        self.patients['238295']['EHR']['Chest pain']='Non-specific'
        self.patients['238295']['EHR']['Prevalence']='Low'
        self.patients['238295']['EHR']['Sex']='Female'
        self.patients['238295']['EHR']['Age']=61
        self.patients['238295']['EHR']['Name']='Ana Murillo'
        self.patients['238295']['EHR']['Smoking']='No'
        self.patients['238295']['EHR']['Diabetes']='No'
        self.patients['238295']['EHR']['Hypertension']='Yes'
        self.patients['238295']['EHR']['Dyslipidaemia']='No'
        self.patients['238295']['EHR']['Previous procedures']=[False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
        self.patients['238295']['EHR']['Urgent study']='No'
        
        self.patients['238295']['Admin']={}
        self.patients['238295']['Admin']['Physician']='Rubén Leta'
        self.patients['238295']['Admin']['Center']='Hospital de la Santa Creu i Sant Pau'
        self.patients['238295']['Admin']['Service']='Cardiology'
        self.patients['238295']['Admin']['Study date']=datetime(2023,10,30).date()
        self.patients['238295']['Quality']='Good'
        self.patients['238295']['Limitations']=[False,False,False,False,False,False,False,False]
        self.patients['238295']['first_filter']=True
        self.patients['238295']['second_filter']=True
        self.patients['238295']['AI suitability']=True
        self.patients['238295']['Dominance']='Right dominance'
        self.patients['238295']['CACs']=0
        self.patients['238295']['Stenosis']={1:['0','LCA'],
                                        2:['0','p-LAD'],
                                        3:['0','m-LAD'],
                                        4:['0','d-LAD'],
                                        5:['0','D1'],
                                        6:['0','D2'],
                                        7:['0','RI'],
                                        8:['0','p-Cx'],
                                        9:['0','d-Cx'],
                                        10:['0','OM1'],
                                        11:['0','OM2'],
                                        12:['0','p-RCA'],
                                        13:['0','m-RCA'],
                                        14:['0','d-RCA'],
                                        15:['0','RPL'],
                                        16:['0','RPD']
                                        }
        ImageInfo_Generator().CADRADS_calculator_individual(self.patients,'238295')
        
        self.patients['50189']={}
        self.patients['50189']['EHR']={}
        self.patients['50189']['EHR']['Consult motive']='Assessment of known coronary artery disease (not revascularized)'
        self.patients['50189']['EHR']['Chest pain']='Atypical'
        self.patients['50189']['EHR']['Prevalence']='Low'
        self.patients['50189']['EHR']['Sex']='Male'
        self.patients['50189']['EHR']['Age']=76
        self.patients['50189']['EHR']['Name']='Cristobal Gil'
        self.patients['50189']['EHR']['Smoking']='Yes'
        self.patients['50189']['EHR']['Diabetes']='Yes'
        self.patients['50189']['EHR']['Hypertension']='Yes'
        self.patients['50189']['EHR']['Dyslipidaemia']='Yes'
        self.patients['50189']['EHR']['Previous procedures']=[False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
        self.patients['50189']['EHR']['Urgent study']='No'
        
        self.patients['50189']['Admin']={}
        self.patients['50189']['Admin']['Physician']='Rubén Leta'
        self.patients['50189']['Admin']['Center']='Hospital de la Santa Creu i Sant Pau'
        self.patients['50189']['Admin']['Service']='Cardiology'
        self.patients['50189']['Admin']['Study date']=datetime(2023,10,30).date()
        self.patients['50189']['Quality']='Good'
        self.patients['50189']['Limitations']=[False,False,False,False,False,False,False,False]
        self.patients['50189']['first_filter']=True
        self.patients['50189']['second_filter']=True
        self.patients['50189']['AI suitability']=True
        self.patients['50189']['Dominance']='Right dominance'
        self.patients['50189']['CACs']=1001
        self.patients['50189']['Stenosis']={1:['1-24','LCA'],
                                        2:['25-49','p-LAD'],
                                        3:['0','m-LAD'],
                                        4:['0','d-LAD'],
                                        5:['25-49','D1'],
                                        6:['0','D2'],
                                        7:['25-49','RI'],
                                        8:['0','p-Cx'],
                                        9:['25-49','d-Cx'],
                                        10:['25-49','OM1'],
                                        11:['25-49','p-RCA'],
                                        12:['25-49','m-RCA'],
                                        13:['50-69','d-RCA'],
                                        14:['25-49','RPL'],
                                        15:['100','RPD']
                                        }
        self.patients['50189']['Plaque segments']={1:['Fibrocalcic','LCA'],
                                        2:['Fibrocalcic','p-LAD'],
                                        3:['Fibrocalcic','D1'],
                                        4:['Fibrocalcic','RI'],
                                        5:['Fibrocalcic','d-Cx'],
                                        6:['Fibrocalcic','OM1'],
                                        7:['Fibrocalcic','p-RCA'],
                                        8:['Fibrocalcic','m-RCA'],
                                        9:['Fibrocalcic','d-RCA'],
                                        10:['Fibrocalcic','RPL'],
                                        11:['Fibrocalcic','RPD']
                                        }
        ImageInfo_Generator().CADRADS_calculator_individual(self.patients,'50189')
        
        self.patients['1951457']={}
        self.patients['1951457']['EHR']={}
        self.patients['1951457']['EHR']['Consult motive']='Screening for coronary artery disease in cardiomyopathy'
        self.patients['1951457']['EHR']['Chest pain']='Non-specific'
        self.patients['1951457']['EHR']['Prevalence']='Low'
        self.patients['1951457']['EHR']['Sex']='Female'
        self.patients['1951457']['EHR']['Age']=55
        self.patients['1951457']['EHR']['Name']='Eva Freixa'
        self.patients['1951457']['EHR']['Smoking']='Yes'
        self.patients['1951457']['EHR']['Diabetes']='No'
        self.patients['1951457']['EHR']['Hypertension']='Yes'
        self.patients['1951457']['EHR']['Dyslipidaemia']='No'
        self.patients['1951457']['EHR']['Previous procedures']=[False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
        self.patients['1951457']['EHR']['Urgent study']='No'
        
        self.patients['1951457']['Admin']={}
        self.patients['1951457']['Admin']['Physician']='Rubén Leta'
        self.patients['1951457']['Admin']['Center']='Hospital de la Santa Creu i Sant Pau'
        self.patients['1951457']['Admin']['Service']='Cardiology'
        self.patients['1951457']['Admin']['Study date']=datetime(2023,10,30).date()
        self.patients['1951457']['Quality']='Good'
        self.patients['1951457']['Limitations']=[False,False,False,False,False,False,False,False]
        self.patients['1951457']['first_filter']=True
        self.patients['1951457']['second_filter']=True
        self.patients['1951457']['AI suitability']=True
        self.patients['1951457']['Dominance']='Right dominance'
        self.patients['1951457']['CACs']=50
        self.patients['1951457']['Stenosis']={1:['0','LCA'],
                                        2:['1-24','p-LAD'],
                                        3:['0','m-LAD'],
                                        4:['0','d-LAD'],
                                        5:['0','D1'],
                                        6:['0','D2'],
                                        7:['0','p-Cx'],
                                        8:['0','d-Cx'],
                                        9:['0','OM1'],
                                        10:['0','OM2'],
                                        11:['0','p-RCA'],
                                        12:['0','m-RCA'],
                                        13:['0','d-RCA'],
                                        14:['0','RPL'],
                                        15:['0','RPD']
                                        }
        self.patients['1951457']['Plaque segments']={
                                        1:['Fibrocalcic','p-LAD'],
                                        2:['Fibrocalcic','D2']
                                        }
        ImageInfo_Generator().CADRADS_calculator_individual(self.patients,'1951457')
        
        self.patients['1042268']={}
        self.patients['1042268']['EHR']={}
        self.patients['1042268']['EHR']['Consult motive']='Screening for coronary artery disease in cardiomyopathy'
        self.patients['1042268']['EHR']['Chest pain']='Non-specific'
        self.patients['1042268']['EHR']['Prevalence']='Low'
        self.patients['1042268']['EHR']['Sex']='Male'
        self.patients['1042268']['EHR']['Age']=67
        self.patients['1042268']['EHR']['Name']='Manuel Costa'
        self.patients['1042268']['EHR']['Smoking']='Yes'
        self.patients['1042268']['EHR']['Diabetes']='No'
        self.patients['1042268']['EHR']['Hypertension']='Yes'
        self.patients['1042268']['EHR']['Dyslipidaemia']='Yes'
        self.patients['1042268']['EHR']['Previous procedures']=[False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
        self.patients['1042268']['EHR']['Urgent study']='No'
        
        self.patients['1042268']['Admin']={}
        self.patients['1042268']['Admin']['Physician']='Rubén Leta'
        self.patients['1042268']['Admin']['Center']='Hospital de la Santa Creu i Sant Pau'
        self.patients['1042268']['Admin']['Service']='Cardiology'
        self.patients['1042268']['Admin']['Study date']=datetime(2023,10,30).date()
        self.patients['1042268']['Quality']='Good'
        self.patients['1042268']['Limitations']=[False,False,False,False,False,False,False,False]
        self.patients['1042268']['first_filter']=True
        self.patients['1042268']['second_filter']=True
        self.patients['1042268']['AI suitability']=True
        self.patients['1042268']['Dominance']='Right dominance'
        self.patients['1042268']['CACs']=1001
        self.patients['1042268']['Stenosis']={1:['0','LCA'],
                                        2:['70-99','p-LAD'],
                                        3:['70-99','m-LAD'],
                                        4:['70-99','d-LAD'],
                                        5:['50-69','D1'],
                                        6:['0','D2'],
                                        7:['0','RI'],
                                        8:['50-69','p-Cx'],
                                        9:['0','d-Cx'],
                                        10:['0','OM1'],
                                        11:['70-99','OM2'],
                                        12:['70-99','p-RCA'],
                                        13:['ND','m-RCA'],
                                        14:['50-69','d-RCA'],
                                        15:['25-49','RPL'],
                                        16:['1-24','RPD']
                                        }
        self.patients['1042268']['Plaque segments']={
                                        1:['Fibrocalcic','p-LAD'],
                                        2:['Fibrocalcic','m-LAD'],
                                        3:['Fibrocalcic','d-LAD'],
                                        4:['Fibrocalcic','D1'],
                                        5:['Fibrocalcic','p-Cx'],
                                        6:['Fibrocalcic','OM2'],
                                        7:['Fibrocalcic','p-RCA'],
                                        8:['Fibrocalcic','m-RCA'],
                                        9:['Fibrocalcic','d-RCA'],
                                        10:['Fibrocalcic','RPL'],
                                        11:['Fibrocalcic','RPD']
                                        }
        ImageInfo_Generator().CADRADS_calculator_individual(self.patients,'1042268')
        
        
        self.patients['1776694']={}
        self.patients['1776694']['EHR']={}
        self.patients['1776694']['EHR']['Consult motive']='Screening for coronary artery disease in cardiomyopathy'
        self.patients['1776694']['EHR']['Chest pain']='Non-specific'
        self.patients['1776694']['EHR']['Prevalence']='Low'
        self.patients['1776694']['EHR']['Sex']='Male'
        self.patients['1776694']['EHR']['Age']=56
        self.patients['1776694']['EHR']['Name']='Josep Castella'
        self.patients['1776694']['EHR']['Smoking']='Yes'
        self.patients['1776694']['EHR']['Diabetes']='No'
        self.patients['1776694']['EHR']['Hypertension']='No'
        self.patients['1776694']['EHR']['Dyslipidaemia']='No'
        self.patients['1776694']['EHR']['Previous procedures']=[False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
        self.patients['1776694']['EHR']['Urgent study']='No'
        
        self.patients['1776694']['Admin']={}
        self.patients['1776694']['Admin']['Physician']='Rubén Leta'
        self.patients['1776694']['Admin']['Center']='Hospital de la Santa Creu i Sant Pau'
        self.patients['1776694']['Admin']['Service']='Cardiology'
        self.patients['1776694']['Admin']['Study date']=datetime(2023,10,30).date()
        self.patients['1776694']['Quality']='Good'
        self.patients['1776694']['Limitations']=[False,False,False,False,False,False,False,False]
        self.patients['1776694']['first_filter']=True
        self.patients['1776694']['second_filter']=True
        self.patients['1776694']['AI suitability']=True
        self.patients['1776694']['Dominance']='Right dominance'
        self.patients['1776694']['CACs']=0
        self.patients['1776694']['Stenosis']={1:['0','LCA'],
                                        2:['0','p-LAD'],
                                        3:['0','m-LAD'],
                                        4:['0','d-LAD'],
                                        5:['0','D1'],
                                        6:['0','D2'],
                                        7:['0','p-Cx'],
                                        8:['0','d-Cx'],
                                        9:['0','OM1'],
                                        10:['0','p-RCA'],
                                        11:['0','m-RCA'],
                                        12:['0','d-RCA'],
                                        13:['0','RPL'],
                                        14:['0','RPD']
                                        }
        ImageInfo_Generator().CADRADS_calculator_individual(self.patients,'1776694')
        
        self.order = PreTestScore().order_prioritization(self.patients)
