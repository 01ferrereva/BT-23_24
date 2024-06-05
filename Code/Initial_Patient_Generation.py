# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 21:31:38 2024

@author: ferbe
"""
import random
from datetime import datetime, timedelta
from faker import Faker

class Initial_Patient_Generation:
    def __init__(self,data_size):
        # number of patients in the cohort
        self.size = data_size 
        
        # 6-digit patient ID
        self.initial_id = str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9)) 
        
        # previous patient procedures with their percentage of incidence
        self.procedures = [('Stent/ACTP',0.0330),
                           ('Coronary bypass',0.0303),
                           ('Pacemaker',0.0029),
                           ('ICD',0.0007),
                           ('Mechanical mitral valve prosthesis',0.0005),
                           ('Biological mitral valve prosthesis',0.0002),
                           ('Mechanical aortic valve prosthesis',0.0009),
                           ('Biological aortic valve prosthesis',0.0003),
                           ('Tricuspid valve prosthesis',0.0001),
                           ('Perceval type aortic valve prosthesis',0.0001),
                           ('Aortic prosthetic tube',0.0026),
                           ('Valved aortic prosthetic tube (Bentall)',0.0004),
                           ('Aortic endoprosthesis',0.0016),
                           ('Left atrial appendage occluder',0.0134),
                           ('Valve leakage shut-off device',0.0003),
                           ('Device for interatrial communications occlusion',0.0003),
                           ('Device for interventricular communications occlusion',0.0000),
                           ('TAVI',0.0022),
                           ('Unspecified percutaneous device',0.0009),
                           ('Corrective surgery for congenital heart disease',0.0005)
                          ]
        
        # motive of patient consultation
        self.consultation_motive = ['Chest pain/atypical symptoms in patient without known CAD',
                                    'No information',
                                    'Checkup, patient without cardiologic symptomatology or known coronary artery disease',
                                    'Suspected acute coronary syndrome (ACS)',
                                    'Alteration myocardial ischemia/perfusion test',
                                    'Nonspecific ECG/Holter alteration',
                                    'Coronary calcification study',
                                    'Assessment of known coronary artery disease (not revascularized)',
                                    'Assessment of revascularized coronary artery disease',
                                    'Screening for coronary artery disease in cardiomyopathy',
                                    'Screening for coronary artery disease in endocarditis',
                                    'Coronary artery disease screening in systemic disease',
                                    'Coronary vein study',
                                    'Coronary anomaly study',
                                    'Other'
                                   ]
        
        # types of chest pain reported
        self.chest_pain = ['Typical',
                           'Atypical',
                           'Non-specific'
                          ]
        
        # percentage of incidence of each consultation motive
        self.weights_motives = [0.2926,
                                0.0792,
                                0.0503,
                                0.0026,
                                0.0043,
                                0.0059,
                                0.0010,
                                0.0224,
                                0.0728,
                                0.0326,
                                0.0019,
                                0.0002,
                                0.0028,
                                0.0020,
                                0.4292
                               ]
        
        self.physicians = ['Abdel Moustafa','Rubén Leta']
        self.centers = ['Hospital de la Santa Creu i Sant Pau']
        self.services = ['Cardiology','Emergency Room']
    
    def random_date(self,start_date, end_date):
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        return start_date + timedelta(days=random_days)

    def generate_initial_patient(self):
        EHR = {} #information of the electronic health records (EHR)
        admin = {} #administrative information
        
        # Possible parameters
        sex = ['Male','Female']
        binary_choice = ['Yes','No']
        
        # Patient generation
        EHR['Consult motive'] = random.choices(self.consultation_motive, weights=self.weights_motives)[0]
        #if EHR['Consult motive'] not in ['No information','Checkup, patient without cardiologic symptomatology or known coronary artery disease']:
        EHR['Chest pain'] = random.choice(self.chest_pain)
        if EHR['Consult motive'] not in ['Assessment of known coronary artery disease (not revascularized)','Assessment of revascularized coronary artery disease']:
            EHR['Prevalence'] = 'Low'
        else:
            EHR['Prevalence'] = 'High'
        EHR['Sex'] = random.choice(sex)
        EHR['Age'] = random.randint(40,90)
        # create instance of Faker in spanish
        fake = Faker('es_ES')
        EHR['Name'] = str(fake.first_name())+' '+str(fake.last_name())
        EHR['Smoking'] = random.choices(binary_choice,weights=(0.17,0.83))[0]
        EHR['Diabetes'] = random.choices(binary_choice,weights=(0.088,0.912))[0]
        EHR['Hypertension'] = random.choices(binary_choice,weights=(0.2385,0.7615))[0]
        EHR['Dyslipidaemia'] = random.choices(binary_choice,weights=(0.2018,0.7982))[0]
        pre_procedures = []
        for i in range(20):
            choice = random.choices([self.procedures[i][0],False],weights=(self.procedures[i][1],1-self.procedures[i][1]))
            pre_procedures.extend(choice)
        EHR['Previous procedures'] = pre_procedures
        EHR['Urgent study'] = random.choices(binary_choice,weights=(0.2,0.8))[0] #case marked by the clinician as an urgent study
        
        admin['Physician'] = random.choice(self.physicians)
        admin['Center'] = random.choice(self.centers)
        admin['Service'] = random.choice(self.services)
        admin['Study date'] = self.random_date(datetime(2023, 1, 1).date(), datetime.now().date())
        
        return EHR,admin

    def generate_initial_pool(self):
        pool_of_patients = {} #pool of patients that make a consult to the hospital
        for i in range(self.size):
            identifier = str(int(self.initial_id) + i) # six digit consecutive unique identifier
            EHR_initial, admin_initial = self.generate_initial_patient() # information depending on the patient
            pool_of_patients[identifier]={}
            pool_of_patients[identifier]['EHR'] = EHR_initial
            pool_of_patients[identifier]['Admin'] = admin_initial

        return pool_of_patients