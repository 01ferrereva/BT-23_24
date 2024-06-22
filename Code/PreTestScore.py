import numpy as np

class PreTestScore:
    def __init__(self):
        # Coefficients for the three different models of Pre-Test probability of CAD:
        self.basic_model_coefficients = [-6.917, # Intercept
                                         0.063,  # Age
                                         1.358,  # Male sex
                                         0.658,  # Atypical chest pain
                                         1.975,  # Typical chest pain
                                         1.065   # Setting
                                        ]
        self.clinical_model_coefficients = [-7.539, # Intercept
                                            0.062,  # Age
                                            1.332,  # Male sex
                                            0.633,  # Atypical chest pain
                                            1.998,  # Typical chest pain
                                            0.828,  # Diabetes
                                            0.338,  # Hypertension
                                            0.422,  # Dyslipidaemia
                                            0.461,  # Smoking
                                            1.049,  # Setting
                                            -0.402  # Combination diabetes and typical chest pain
                                           ]  
        self.CCS_model_coefficients = [-5.975, # Intercept
                                       0.011,  # Age
                                       0.786,  # Male sex
                                       0.718,  # Atypical chest pain
                                       2.024,  # Typical chest pain
                                       0.658,  # Diabetes
                                       0.235,  # Hypertension
                                       0.185,  # Dyslipidaemia
                                       0.207,  # Smoking
                                       0.577,  # Log transformed CCS
                                       1.566,  # Setting
                                       -0.157, # Combination of setting and CCS
                                       -0.780  # Combination of diabetes and typical chest pain
                                      ]
        
    # Calculate first the linear function of the models
    def linear_function(self,patient):
        age = patient['EHR']['Age']
        sex = 1 if patient['EHR']['Sex']=='Male' else 0 
        prevalence = 1 if patient['EHR']['Prevalence']=='High' else 0
        
        # test if the patient has chest pain:
        try: 
            typical_chest_pain = 1 if patient['EHR']['Chest pain']=='Typical' else 0
            atypical_chest_pain = 1 if patient['EHR']['Chest pain']=='Atypical' else 0
        except:
            typical_chest_pain = 0
            atypical_chest_pain = 0
        
        # test if the patient has (all) risk factors inputed for clinical model, otherwise use basic model:
        try:
            diabetes = 1 if patient['EHR']['Diabetes']=='Yes' else 0
            combination_diabetes_typical_chest_pain = 1 if (diabetes==1 and typical_chest_pain==1) else 0
        except:
            return ('Basic',np.dot(self.basic_model_coefficients,[1,age,sex,atypical_chest_pain,typical_chest_pain,prevalence]))
        try:
            #hypertension = 1 if (patient['EHR']['BP'][0]>139 or patient['EHR']['BP'][1]>89) else 0
            hypertension = 1 if patient['EHR']['Hypertension']=='Yes' else 0
        except:
            return ('Basic',np.dot(self.basic_model_coefficients,[1,age,sex,atypical_chest_pain,typical_chest_pain,prevalence]))
        try:
            dyslipidaemia = 1 if patient['EHR']['Dyslipidaemia']=='Yes' else 0
        except:
            return ('Basic',np.dot(self.basic_model_coefficients,[1,age,sex,atypical_chest_pain,typical_chest_pain,prevalence]))
        try:
            smoking = 1 if patient['EHR']['Smoking']=='Yes' else 0
        except:
            return ('Basic',np.dot(self.basic_model_coefficients,[1,age,sex,atypical_chest_pain,typical_chest_pain,prevalence]))
        
        # test if the patient has a coronary artery calcium score (CACs) for CCS model, otherwise use clinical model:
        try:
            cacs = np.log(patient['CACs']) # natural logarithm of CACs value
            combination_setting_CCS = cacs if prevalence==1 else 0
        except:
            return ('Clinical',np.dot(self.clinical_model_coefficients,[1,age,sex,atypical_chest_pain,typical_chest_pain,diabetes,hypertension,dyslipidaemia,smoking,prevalence,combination_diabetes_typical_chest_pain]))
        
        return ('CCS',np.dot(self.CCS_model_coefficients,[1,age,sex,atypical_chest_pain,typical_chest_pain,diabetes,hypertension,dyslipidaemia,smoking,cacs,prevalence,combination_setting_CCS,combination_diabetes_typical_chest_pain]))
    
    # Calculate probability of CAD using the corresponding model
    def pre_test_model(self,patient):
        model_type,argument = self.linear_function(patient)
        pre_test_score = round(100*(np.exp(argument)/(1+np.exp(argument))),2)
        return (model_type,pre_test_score)
    
    # Add the probability of CAD calculated using the Pre-Test score, and the model used to calculate it in the patient database
    def assign_risk(self,database):
        for i in database:
            model_type, pre_test_score = self.pre_test_model(database[i])
            database[i]['Model type'] = model_type
            database[i]['Pre-test score'] = pre_test_score
        return database
    
    # Order a pool of patients depending on the value of their CAD probability
    def order_prioritization(self,database):
        database = self.assign_risk(database)
        order = []
        for i in database:
            patient = []
            patient.append(i)
            patient.append(database[i]['EHR']['Age'])
            patient.append(database[i]['EHR']['Sex'])
            try: 
                patient.append(database[i]['EHR']['Chest pain'])
            except:
                patient.append('No chest pain')
            
            if database[i]['Model type'] != 'Basic model':
                patient.append(database[i]['EHR']['Diabetes'])
                patient.append(database[i]['EHR']['Hypertension'])
                patient.append(database[i]['EHR']['Dyslipidaemia'])
                patient.append(database[i]['EHR']['Smoking'])
            else: 
                patient.extend(['-','-','-','-'])
                
            if database[i]['Model type'] == 'CCS model':
                patient.append(database[i]['CACs'])
            else:
                patient.append('-')
                
            patient.append(database[i]['Model type'])
            patient.append(database[i]['Pre-test score'])
            try: 
                patient.append(database[i]['Admin']['Scheduled_img'])
            except: 
                pass
            
            order.append(patient)
            
        order = sorted(order, key=lambda x:x[10], reverse=True) # order sorted by descending CAD probability
        
        return order