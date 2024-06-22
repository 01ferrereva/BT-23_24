import sys
import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import nibabel as nib
import open3d as o3d

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QLabel, QLineEdit, QFileDialog, QVBoxLayout, QWidget, QSlider, QDockWidget, QComboBox
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QDate
from PyQt5.QtCore import Qt

from Initial_Patient_Generation import Initial_Patient_Generation
from PreTestScore import PreTestScore
from ImageAcquisition import ImageAcquisition
from Filtering import Filtering
from ImageInfo_Generator import ImageInfo_Generator
from Report_Generation import Report_Generation
from Prioritization_Validation import Prioritization_Validation

"""
BASELINE CODE: 
    Code to generate the database of the patients which will be ordered for CCTA acquisition and reporting
"""
class main:
    # initial batch of patients of 15
    def __init__(self,num_patients=15):
        
        # generate the initial pool of patients (15)
        self.initial_patients = Initial_Patient_Generation(num_patients).generate_initial_pool()
        
        # order this initial pool of patients by highest probability of CAD for image acquisition
        self.set_order4image(self.initial_patients)
        
        # generate, for each patient, information related to the image acquisition technique (quality, artifacts,...)
        self.set_imageAcquisition(self.initial_patients,self.get_order4image())
        
        # filter patients that will be suitable for an automatic image analysis algorithm
        self.set_filtering(self.get_imageAcquisition())
        
        # generate the image information that would be, in theory, extracted from this automatic image analysis algorithm (only for the suitable patients)
        self.set_imgAnalysis(self.get_filtering()[0])
        
        # order all patients depending on image findings (if available) and other prior information for clinical assessment
        self.set_order4validation(self.get_imgAnalysis(),self.get_filtering()[1])
        
    def set_order4image(self,dic):
        self.__order4image = PreTestScore().order_prioritization(dic)
    def get_order4image(self):
        return self.__order4image
        
    def set_imageAcquisition(self,dic,order):
        self.__imageAcquisition = ImageAcquisition().take_ccta(dic,order)
    def get_imageAcquisition(self):
        return self.__imageAcquisition
    
    def set_filtering(self,dic):
        self.__filtering1, self.__filtering2 = Filtering().filtering(dic)
    def get_filtering(self):
        return self.__filtering1,self.__filtering2
    
    def explain_filtering(self,dic,identifier):
        return Filtering().explainability_suitability(dic,identifier)
    
    def set_imgAnalysis(self,dic):
        analysed_patient_images = ImageInfo_Generator().image_data_generator(dic) # generate image information 
        analysed_patient_images = PreTestScore().assign_risk(analysed_patient_images) # recalculate the PreTest Score with all the available data
        analysed_patient_images = ImageInfo_Generator().CADRADS_calculator(analysed_patient_images) # calculate the CAD-RADS with the image information
        self.__imgAnalysis = analysed_patient_images
    def get_imgAnalysis(self):
        return self.__imgAnalysis
    
    def set_order4validation(self,dic_AI,dic_notAI):
        self.__order4validation = Prioritization_Validation(dic_AI,dic_notAI).set_order()
    def get_order4validation(self):
        return self.__order4validation
    
    def set_reportGeneration(self,dic,identifier):
        self.__reportGeneration = Report_Generation().final_reporting(dic,identifier)
    def get_reportGeneration(self):
        return self.__reportGeneration
    
    order4image = property(get_order4image,set_order4image)
    imageAcquisition = property(get_imageAcquisition,set_imageAcquisition)
    filtering = property(get_filtering,set_filtering)
    imgAnalysis = property(get_imgAnalysis,set_imgAnalysis)
    order4validation = property(get_order4validation,set_order4validation)
    reportGeneration = property(get_reportGeneration,set_reportGeneration)

"""
LOGIN OF PHYSICIAN FOR REPORTING:
    Login window for physicians to the reporting system
"""
class LogIn(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('gui_login.ui', self)
        
        self.main_class = main() 
        
        # User
        self.user.setPlaceholderText("Enter user here")
        self.user.textChanged.connect(self.check_enable_button) # check whether enter button can be activated
        
        # Password
        self.password.setPlaceholderText("Enter password here")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.textChanged.connect(self.check_enable_button) # check whether enter button can be activated
        
        # Enter 
        self.Enter.setEnabled(False)
        self.Enter.clicked.connect(self.check_dictionary)
        self.password.returnPressed.connect(self.check_dictionary) # check that user and password are in the password database
        
        # User and password dictionary, with the respective action permissions of each user
        self.password_dic = {'test': ['password', ['generate', 'acquire', 'report']]}
    
    # Check that user and password are filled to enable the enter button
    def check_enable_button(self):
        text1 = self.user.text().strip()
        text2 = self.password.text().strip()
        self.Enter.setEnabled(bool(text1 and text2))
    
    # check that the user has permissions to perform the requested action (register/search patients, schedule CCTA acquisition, report CCTA cases)
    def check_permissions(self):
        user = self.user.text().strip()
        permissions = self.password_dic.get(user, [None, []])[1]
        return permissions
    
    # Check that the user is in the dictionary, and that the password corresponds to the one of this user (raise an alert otherwise) 
    def check_dictionary(self):
        text1 = self.user.text().strip()
        text2 = self.password.text().strip()
        if text1 in self.password_dic:
            if text2 == self.password_dic[text1][0]:
                self.close()
                self.activities_window = Activities(self)
                self.activities_window.show()
            else:
                QMessageBox.warning(self, "Incorrect Password", "The password is incorrect.")
        else:
            QMessageBox.warning(self, "Incorrect User", "The user does not exist.")

"""
ACTIVITIES WINDOW:
    Window to choose which action the physician wants to take; whether they want to register a new patient in the system,
    they want to search the information of an already existing patient, they want to see the list of ordered patients for 
    CCTA acquisition, or they want to open the list for CCTA assessment to report the cases.
"""
class Activities (QMainWindow):
    def __init__(self,parent):
        super().__init__()
        uic.loadUi('gui_choose_action.ui',self)   
        self.setWindowTitle('Actions')
        self.parent = parent
        self.main_class = self.parent.main_class
        
        self.generate.clicked.connect(self.generate_checked) # chosen register new patient or search patient
        self.acquire.clicked.connect(self.acquire_checked) # chosen list for acquisition of CCTAs
        self.report.clicked.connect(self.report_checked) # chosen list for CCTA reporting
    
    # Check whether the physician in the database has permissions to perform the selected action and if so, open the new corresponding window
    def generate_checked(self):
        if 'generate' in self.parent.check_permissions():
            self.home_window = Home(self)
            self.home_window.show()
        else:
            QMessageBox.warning(self, "No permissions", "The user does not have permissions for this action.")
    
    def acquire_checked(self):
        if 'acquire' in self.parent.check_permissions():
            self.acquire_ccta = AcquisitionList(self)
            self.acquire_ccta.show()
        else:
            QMessageBox.warning(self, "No permissions", "The user does not have permissions for this action.")
    
    def report_checked(self):
        if 'report' in self.parent.check_permissions():
            self.workinglist_window = WorkingList(self)
            self.workinglist_window.show()
        else:
            QMessageBox.warning(self, "No permissions", "The user does not have permissions for this action.")

"""
HOME WINDOW: 
    If action chosen was register/search a new patient, now physician can choose if they want to register a new patient or 
    they want to search an existing patient.
"""
class Home (QMainWindow):
    def __init__(self,parent):
        super().__init__()
        uic.loadUi('gui_Home.ui',self)   
        self.setWindowTitle('Home')
        self.parent = parent
        self.main_class = self.parent.main_class
        
        self.new_p.clicked.connect(self.new_patient) # chosen register a new patient
        self.search_p.clicked.connect(self.search_patient) # chosen search an existing patient
    
    # Depending on the choice, open the corresponding window of the action
    def new_patient(self):
        self.create_window = Register(self)
        self.create_window.show()
    
    def search_patient(self):
        self.search_window = Search(self)
        self.search_window.show()

"""
REGISTER NEW PATIENTS: 
    Reporting system with the options to input clinical and demographic information from a new patient, manually by the 
    clinician. The unique identifier of this new patient is automatically generated by the system. 
"""
class Register(QMainWindow):
    def __init__(self,parent):
        super().__init__(parent)
        uic.loadUi('gui_report_clinical.ui',self)
        self.setWindowTitle('Register Patient')
        self.parent = parent
        self.main_class = self.parent.main_class
        
        self.ident = str(int(sorted(self.main_class.initial_patients.keys())[-1])+1) # automatically generated ID
        self.textID.setText(str(self.ident))
        self.textID.setEnabled(False) # make that this information is non-modifiable
        
        self.register_button.clicked.connect(self.registered_patient) 
    
    # gather the information inputted by the clinician and add it into the patient database in the same format
    def registered_patient(self):
        EHR = {}
        admin =  {}
        EHR['Consult motive'] = self.motive.currentText()
        EHR['Prevalence'] = self.prevalence.currentText()
        if self.FemaleSex.isChecked():
            EHR['Sex'] = 'Female'
        elif self.MaleSex.isChecked():
            EHR['Sex'] = 'Male'
        else:
            EHR['Sex'] = ''
        EHR['Age'] = int(self.textAge.text())
        EHR['Chest pain'] = self.chestpain.currentText()
        EHR['Name'] = self.name.text()
        EHR['Smoking'] = self.smoking.isChecked()
        EHR['Diabetes'] = self.diabetes.isChecked()
        EHR['Hypertension'] = self.hypertension.isChecked()
        EHR['Dyslipidaemia'] = self.dyslipidaemia.isChecked()
        EHR['Previous procedures'] = self.prepro.currentText()
        EHR['Urgent study'] = self.UrgentStudy.isChecked()
        admin['Physician'] = self.textPhysician.text()
        admin['Center'] = self.textHospital.text()
        admin['Service'] = self.textService.text()
        admin['Study date'] = self.dateStudy.date()
        
        self.main_class.initial_patients[self.ident] = {}
        self.main_class.initial_patients[self.ident]['EHR'] = EHR
        self.main_class.initial_patients[self.ident]['Admin'] = admin
        
        QMessageBox.information(self, "Successful registration", 'The patient has been successfully registered') 

"""
SEARCH PATIENT:
    Reporting system with the option to input an ID and shows the information related to the patient to which ID corresponds.
"""
class Search(QMainWindow):
    def __init__(self,parent):
        super().__init__(parent)
        uic.loadUi('gui_report_clinical.ui',self)
        self.setWindowTitle('Search Patient')
        self.parent = parent
        self.main_class = self.parent.main_class
        
        self.textID.setStyleSheet("background-color: red; color: white; font-weight: bold") # only modifiable field
        
        self.textAge.setEnabled(False)
        self.name.setEnabled(False)
        self.smoking.setEnabled(False)
        self.diabetes.setEnabled(False)
        self.motive.setEnabled(False)
        self.prevalence.setEnabled(False)
        self.FemaleSex.setEnabled(False)
        self.MaleSex.setEnabled(False)
        self.hypertension.setEnabled(False)
        self.dyslipidaemia.setEnabled(False)
        self.prepro.setEnabled(False)
        self.UrgentStudy.setEnabled(False)
        self.textPhysician.setEnabled(False)
        self.textHospital.setEnabled(False)
        self.textService.setEnabled(False)
        self.chestpain.setEnabled(False)
        self.dateStudy.setEnabled(False)
        
        self.ident = self.textID.text().strip()
        self.textID.textChanged.connect(self.get_id) # if information is inputted in the ID field, gather this information
        
        self.register_button.setText('SEARCH')
        self.register_button.clicked.connect(self.search_patient) # search ID inputted in the patient database
    
    def get_id(self):
        self.ident = self.textID.text().strip()
    
    # search information in the patient database and fill it in the appropriate fields of the reporting system
    def search_patient(self):
        self.ident = self.textID.text().strip()
        if self.ident in self.main_class.initial_patients.keys(): 
            self.textID.setEnabled(False)
            self.name.setText(self.main_class.initial_patients[self.ident]['EHR']['Name'])
            self.dateStudy.setDate(self.main_class.initial_patients[self.ident]['Admin']['Study date'])
            self.textAge.setText(str(self.main_class.initial_patients[self.ident]['EHR']['Age']))
            try: 
              self.smoking.setChecked(self.main_class.initial_patients[self.ident]['EHR']['Smoking'])
            except:
                self.smoking.setChecked(True if self.main_class.initial_patients[self.ident]['EHR']['Smoking']=='Yes' else False)
            try:
                self.diabetes.setChecked(self.main_class.initial_patients[self.ident]['EHR']['Diabetes'])
            except:
                self.diabetes.setChecked(True if self.main_class.initial_patients[self.ident]['EHR']['Diabetes']=='Yes' else False)
            try:
                self.hypertension.setChecked(self.main_class.initial_patients[self.ident]['EHR']['Hypertension'])
            except:
                self.hypertension.setChecked(True if self.main_class.initial_patients[self.ident]['EHR']['Hypertension']=='Yes' else False)
            try:
                self.dyslipidaemia.setChecked(self.main_class.initial_patients[self.ident]['EHR']['Dyslipidaemia'])
            except:
                self.dyslipidaemia.setChecked(True if self.main_class.initial_patients[self.ident]['EHR']['Dyslipidaemia']=='Yes' else False)
            self.motive.setCurrentText(self.main_class.initial_patients[self.ident]['EHR']['Consult motive'])
            try:
                self.UrgentStudy.setChecked(self.main_class.initial_patients[self.ident]['EHR']['Urgent study'])
            except:
                self.UrgentStudy.setChecked(True if self.main_class.initial_patients[self.ident]['EHR']['Urgent study']=='Yes' else False)
            self.textPhysician.setText(self.main_class.initial_patients[self.ident]['Admin']['Physician'])
            self.textHospital.setText(self.main_class.initial_patients[self.ident]['Admin']['Center'])
            self.textService.setText(self.main_class.initial_patients[self.ident]['Admin']['Service'])
            self.prevalence.setCurrentText(self.main_class.initial_patients[self.ident]['EHR']['Prevalence'])
            self.MaleSex.setChecked(True if self.main_class.initial_patients[self.ident]['EHR']['Sex']=='Male' else False)
            self.FemaleSex.setChecked(True if self.main_class.initial_patients[self.ident]['EHR']['Sex']=='Female' else False)
            self.chestpain.setCurrentText(self.main_class.initial_patients[self.ident]['EHR']['Chest pain'])
            try:
                self.prepro.setCurrentText(self.main_class.initial_patients[self.ident]['EHR']['Previous procedures'])
            except:
                prepro = [x for x in self.main_class.initial_patients[self.ident]['EHR']['Previous procedures'] if x is not False]
                try:
                    self.prepro.setCurrentText(prepro[0])
                except:
                    pass
        else:
            QMessageBox.warning(self,'Inexistent patient','There is no patient with this ID.') # if the ID inputted is not in the patient database

"""
ORDERED CCTA ACQUISITION LIST:
    List of patients (the initial 15) which have been ordered from higher probability of suffering CAD to lower probability
    of suffering CAD calculated by the Pre-Test Score. This list indicates for each patient the value of the variables considered
    for the calculation of this probability (e.g. Age, Sex, Diabetes,...). This serves as explainability for patient order.
"""
class AcquisitionList (QMainWindow):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi('gui_acquisition_list.ui',self)
        self.setWindowTitle('CCTA Acquisition List')
        
        self.grid_layout = self.gridLayout
        
        self.parent = parent
        self.main_class = self.parent.parent.main_class
        order = self.main_class.get_order4image() # method to extract the order for patient CCTA acquisition
        num_patients = len(order)
        
        # information for each column of the grid for each patient
        for i in range(num_patients):
            prev_order = order[i][11] # initial scheduled order
            current_order = f'{i+1}' # current calculated order
            n_order = current_order + ' (before: '+str(prev_order)+')'
            num_order = QLabel(n_order)
            num_order.setAlignment(QtCore.Qt.AlignCenter)
            
            ident = QLabel(order[i][0]) # unique ID
            ident.setAlignment(QtCore.Qt.AlignCenter)
            
            age = QLabel(str(order[i][1])) # age (in years)
            age.setAlignment(QtCore.Qt.AlignCenter)
            
            sex = QLabel(order[i][2]) # sex (Male/Female)
            sex.setAlignment(QtCore.Qt.AlignCenter)
            
            chest_pain = QLabel(order[i][3]) # chest pain (Typical/Atypical/Non-specific)
            chest_pain.setAlignment(QtCore.Qt.AlignCenter)
            
            diabetes = QLabel(order[i][4]) # diabetes (yes/no)
            diabetes.setAlignment(QtCore.Qt.AlignCenter)
            
            hta = QLabel(order[i][5]) # hypertension (yes/no)
            hta.setAlignment(QtCore.Qt.AlignCenter)
            
            dysli = QLabel(order[i][6]) # dyslipidemia (yes/no)
            dysli.setAlignment(QtCore.Qt.AlignCenter)
            
            smoke = QLabel(order[i][7]) # smoking (yes/no)
            smoke.setAlignment(QtCore.Qt.AlignCenter)
            
            cacs = QLabel(order[i][8]) # coronary artery calcium score
            cacs.setAlignment(QtCore.Qt.AlignCenter)
            
            model = QLabel(order[i][9]) # type of model used for the calculation of CAD probability (basic/clinical/calcium)
            model.setAlignment(QtCore.Qt.AlignCenter)
            
            risk = QLabel(str(order[i][10])) # calculated probability of CAD
            risk.setAlignment(QtCore.Qt.AlignCenter)
            
            # set values in grid
            self.grid_layout.addWidget(num_order,i+2,4)
            self.grid_layout.addWidget(ident,i+2,5)
            self.grid_layout.addWidget(age,i+2,6)
            self.grid_layout.addWidget(sex,i+2,7)
            self.grid_layout.addWidget(chest_pain,i+2,8)
            self.grid_layout.addWidget(diabetes,i+2,9)
            self.grid_layout.addWidget(hta,i+2,10)
            self.grid_layout.addWidget(dysli,i+2,11)
            self.grid_layout.addWidget(smoke,i+2,12)
            self.grid_layout.addWidget(cacs,i+2,13)
            self.grid_layout.addWidget(model,i+2,14)
            self.grid_layout.addWidget(risk,i+2,15)

"""
ORDERED WORK LIST OF EACH PHYSICIAN:
    List of patients (the initial 15) which have been ordered from higher priority for image assessement to lower priority for
    image assessment. This priority is calculated according to clinical criteria using CCTA image findings (in the cases where
    the automatic image could be performed) and previous information.
"""
class WorkingList (QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi('gui_worklist4.ui',self)
        self.setWindowTitle('Working List')
        
        self.grid_layout = self.gridLayout
        
        self.parent = parent
        self.main_class = self.parent.parent.main_class
        order = self.main_class.get_order4validation() # method to extract the order for patient CCTA assessment
        num_patients = len(order)
        
        # information for each column of the grid for each patient
        for i in range(num_patients):
            ident = order[i][0] # unique ID
            info = QPushButton("+") # button for more information about the patient and explainability of the order
            
            # scheduled prior order and calculated current order
            current = f"{i+1}"
            if ident in self.main_class.get_imgAnalysis().keys():
                prior = self.main_class.get_imgAnalysis()[ident]['Admin']['Scheduled_img']
            elif ident in self.main_class.get_filtering()[1].keys():
                prior = self.main_class.get_filtering()[1][ident]['Admin']['Scheduled_img']
            final = current + ' (before: '+str(prior)+')'
            num_order = QLabel(final)
            num_order.setAlignment(QtCore.Qt.AlignCenter)
            
            name = QLabel(order[i][1]) # patient's name (automatically generated)
            name.setAlignment(QtCore.Qt.AlignCenter)
            
            urgency = QLabel(order[i][2]) # classification of the severity of patient (CRITICAL / HIGH / MEDIUM / LOW)
            urgency.setAlignment(QtCore.Qt.AlignCenter)
            
            cadrads = QLabel(order[i][3]) # value of CAD-RADS
            cadrads.setAlignment(QtCore.Qt.AlignCenter)
            
            motive = QLabel(order[i][7]) # initial motive of consultation
            
            urg_std = QLabel(str(order[i][8])) # whether case is marked as urgent (coming from the ER)
            urg_std.setAlignment(QtCore.Qt.AlignCenter)
            
            # add if patient has stent/graph or some artifact which makes the study suboptimal
            notes_info = [x for x in order[i][4] if x!='-']
            if order[i][9]!=[]:
                notes_info.append('Suboptimal')
            
            # add if patient has deficient image quality which makes the study suboptimal
            if ident in self.main_class.get_imgAnalysis().keys():
                if self.main_class.get_imgAnalysis()[ident]['Quality'] == 'Deficient':
                    notes_info.append('Suboptimal')
            elif ident in self.main_class.get_filtering()[1].keys():
                if self.main_class.get_filtering()[1][ident]['Quality'] == 'Deficient':
                    notes_info.append('Suboptimal')
            
            # report these notes 
            notes_info = list(set(notes_info))
            if notes_info!=[]:
                for k in notes_info: 
                    if k == notes_info[0]:
                        note = str(k)
                    else:
                        note = ", ".join((note,k))
            else: 
                note = ""
            notes = QLabel(note)
            notes.setStyleSheet("color: red; font-weight: bold")
            
            # label of buttons call2action depending whether the patient has/has not preliminary report
            if order[i][3] != "-":
                action = QPushButton("Validate")
            else:
                action = QPushButton("Report")
            
            # coloring of priority groups
            if order[i][2] == "Critical priority":
                urgency.setStyleSheet("color: red; font-weight: bold")
                urgency.setText('CRITICAL')
                cadrads.setText(order[i][3]+'*')
                cadrads.setStyleSheet('font-weight: bold')
            elif order[i][2] == "High priority":
                urgency.setStyleSheet("color: orange; font-weight: bold")
                urgency.setText('HIGH')
            elif order[i][2] == "Medium priority":
                urgency.setStyleSheet("color: #e8bc3b; font-weight:bold")
                urgency.setText('MEDIUM')
            else:
                urgency.setStyleSheet("color: green; font-weight: bold")
                urgency.setText('LOW')
            
            # mark in bold the cases that are first because they are marked as urgent
            if order[i][8] == True:
                urg_std.setStyleSheet("background-color: red; color: white; font-weight: bold")
            
            action.clicked.connect(lambda _, ident=ident: self.on_button_clicked(ident)) # call2action (report/validate)
            info.clicked.connect(lambda _, ident=ident: self.explainability_more_info(ident)) # explainability of patient order
            
            # set values in grid
            self.grid_layout.addWidget(urg_std,i+2,2)
            self.grid_layout.addWidget(num_order,i+2,3)
            self.grid_layout.addWidget(name,i+2,4)
            self.grid_layout.addWidget(urgency,i+2,5)
            self.grid_layout.addWidget(cadrads,i+2,6)
            self.grid_layout.addWidget(motive,i+2,7)
            self.grid_layout.addWidget(notes,i+2,8)
            self.grid_layout.addWidget(info,i+2,9)
            self.grid_layout.addWidget(action,i+2,10)
            
    # call2action button opening window with preliminary case report to validate/finish reporting
    def on_button_clicked(self, identifier):
        global report_coronaries
        report_coronaries = ReportCoronaries(identifier,self.main_class)
        report_coronaries.setGeometry(0,0,1250,900)
        report_coronaries.show()
    
    # explainability of order of patients
    def explainability_more_info(self,identifier):
        if identifier in self.main_class.get_imgAnalysis().keys():
            global more_info
            more_info = Exp_order_AI(self,identifier)
            more_info.show()
        elif identifier in self.main_class.get_filtering()[1].keys():
            global more_info2
            more_info2 = Exp_order_nonAI(self,identifier)
            more_info2.show()

"""
EXPLAINABILITY OF WORKING LIST ORDER:
    Visual window reporting clinical information about the patient, as well as image findings such as findings from the main 
    coronary vessels (from patients going through automatic image analysis). This information is given to further justify the 
    order of the patients in the CCTA assessment list.
"""
# Explainability for patients going through AI-workflow
class Exp_order_AI (QMainWindow):
    def __init__(self,parent,identifier):
        super().__init__(parent)
        uic.loadUi('gui_PriorityExp_AI.ui',self)
        self.setWindowTitle('Explainability')
        self.setGeometry(10,100,650,750)
        
        self.ident = identifier
        self.main_class = parent.main_class
        
        # gather all clinical and image-related information to report it in the explainability window
        
        # No image-related information: motive of consultation, type of chest paint, previous procedures, requested from the ER, pre-test score,...
        consult_motive = self.main_class.get_imgAnalysis()[self.ident]['EHR']['Consult motive']
        try:
            chest_pain = self.main_class.get_imgAnalysis()[self.ident]['EHR']['Chest pain']
        except:
            chest_pain = 'No'
        previous_proc = self.main_class.get_imgAnalysis()[self.ident]['EHR']['Previous procedures']
        previous_proc_list = [x for x in previous_proc if x is not False]
        pre_test_score = self.main_class.get_imgAnalysis()[self.ident]['Pre-test score']
        urgency = self.main_class.get_imgAnalysis()[self.ident]['EHR']['Urgent study']
        
        # Image-related information: CAD-RADS, >=70% in main vessels, CACs, maximum range of stenosis in main vessels and their cMPRs.
        CADRADS = self.main_class.get_imgAnalysis()[self.ident]['CADRADS']
        alarm = self.main_class.get_imgAnalysis()[self.ident]['Alarm']
        CACS = self.main_class.get_imgAnalysis()[self.ident]['CACs']
        
        LAD_stenosis = []
        Cx_stenosis = []
        RCA_stenosis = []
        
        for i in self.main_class.get_imgAnalysis()[self.ident]['Stenosis']:
            value = self.main_class.get_imgAnalysis()[self.ident]['Stenosis'][i]
            if value[1]=='p-LAD' or value[1]=='m-LAD' or value[1]=='d-LAD':
                LAD_stenosis.append(value[0])
            elif value[1]=='p-Cx' or value[1]=='m-Cx' or value[1]=='d-Cx':
                Cx_stenosis.append(value[0])
            elif value[1]=='p-RCA' or value[1]=='m-RCA' or value[1]=='d-RCA':
                RCA_stenosis.append(value[0])
        
        self.LAD = max(LAD_stenosis)
        self.Cx = max(Cx_stenosis)
        self.RCA = max(RCA_stenosis)
        
        # Reporting of the information gathered above
        self.clinical_info_text.setText(f'- Patient presenting {chest_pain} chest pain and under the consultation motive: {consult_motive}.\n- Patient has a Pre-Test Risk Score of {pre_test_score}%.')
        if previous_proc_list == []:
            self.clinical_info_text.append('- Patient does not have any previous procedures reported.')
        else:
            previous_proc_text = []
            self.append_string_with_space(self,previous_proc_text,'- Patient has the following previous procedures reported:')
            for i in previous_proc_list:
                self.append_string_with_space(self,previous_proc_text,str(i))
            self.clinical_info_text.append("".join(previous_proc_text))
        if urgency == 'No':
            self.clinical_info_text.append('- Study was not an urgent request.')
        else:
            self.clinical_info_text.append('- Study was an URGENT request.')
            
        stenosis_text = []
        self.append_string_with_space(stenosis_text,f'Patient has a CAD-RADS value of {CADRADS}')
        if alarm != []:
            self.append_string_with_space(stenosis_text,'with an alarming stenosis in')
            for i in alarm:
                self.append_string_with_space(stenosis_text,str(i[0]))
                if i == alarm[-1]:
                    self.append_string_with_space(stenosis_text,'.')
                else:
                    self.append_string_with_space(stenosis_text,',')
        self.image_info_text.setPlainText("".join(stenosis_text)) 
        self.image_info_text.append(f'Maximum stenosis degrees of the main vessels are LAD={self.LAD}, Cx={self.Cx} and RCA={self.RCA}.')
        self.image_info_text.append(f'\nPatient presents a detected calcium score of {CACS} through Agatston score.')
        
        self.clinical_info_text.setEnabled(False)
        self.image_info_text.setEnabled(False)
        
        # plot (if images available) the cMPRs of the main vessels
        try: 
            self.LAD_CPR.setPixmap(self.CPR_vessel('LAD'))
            self.Cx_CPR.setPixmap(self.CPR_vessel('Cx'))
            self.RCA_CPR.setPixmap(self.CPR_vessel('RCA'))
        except:
            pass
    
    # method to plot the cMPRs of the main vessels (in .png)
    def CPR_vessel(self,vessel_name):
        if vessel_name == 'LAD':
            vessel_affectation = self.LAD
        elif vessel_name == 'Cx':
            vessel_affectation = self.Cx
        elif vessel_name == 'RCA':
            vessel_affectation = self.RCA
            
        if vessel_affectation == '0':
            vessel = 'noCAD'
        elif vessel_affectation == '1-24':
            vessel = 'minimalCAD'
        elif vessel_affectation == '25-49':
            vessel = 'mildCAD'
        elif vessel_affectation == '50-69':
            vessel = 'moderateCAD'
        elif vessel_affectation == '70-99':
            vessel = 'severeCAD'
        elif vessel_affectation == '100':
            vessel = 'obstructiveCAD'
        else:
            vessel = ''
                 
        if vessel != '':
            try: 
                directory = os.getcwd()
                
                # Attention!!! If original images are not available but you want to test this part of the code,
                # try to get screenshoots of cMPRs of coronary vessels and save them in the same directory of this code.
                # Inside this directory, a folder called 'CPR' must be created where this screenshoots will be saved.
                # Each screenshot must be saved with the degree of CAD. (e.g. 'moderateCAD.png', 'mildCAD.png',...).
                cpr_path = os.path.join(directory, 'CPR',vessel)
                
                cpr_image = cpr_path+'.png'
                pixmap = QPixmap(cpr_image)
            except: 
                pass
        else:
            pixmap = QPixmap()
        return pixmap
        
    # method to join information for the report
    def append_string_with_space(self,list_of_strings,string):
        list_of_strings.append(string)
        list_of_strings.append(" ")


# Explainability for patients not going through AI-workflow
class Exp_order_nonAI (QMainWindow):
    def __init__(self,parent,identifier):
        super().__init__(parent)
        uic.loadUi('gui_PriorityExp_nonAI.ui',self)
        self.setWindowTitle('Explainability')
        self.setGeometry(10,100,650,350)
        
        self.ident = identifier
        self.main_class = parent.main_class
        
        # gather all clinical and image-related information to report it in the explainability window
        
        # No image-related information: motive of consultation, type of chest paint, previous procedures, requested from the ER, pre-test score,...
        consult_motive = self.main_class.get_filtering()[1][self.ident]['EHR']['Consult motive']
        try:
            chest_pain = self.main_class.get_filtering()[1][self.ident]['EHR']['Chest pain']
        except:
            chest_pain = 'No'
        previous_proc = self.main_class.get_filtering()[1][self.ident]['EHR']['Previous procedures']
        previous_proc_list = [x for x in previous_proc if x is not False]
        pre_test_score = self.main_class.get_filtering()[1][self.ident]['Pre-test score']
        urgency = self.main_class.get_filtering()[1][self.ident]['EHR']['Urgent study']
        
        self.clinical_info_text.setText(f'- Patient presenting {chest_pain} chest pain and under the consultation motive: {consult_motive}.\n- Patient has a Pre-Test Risk Score of {pre_test_score}%.')
        if previous_proc_list == []:
            self.clinical_info_text.append('- Patient does not have any previous procedures reported.')
        else:
            previous_proc_text = []
            self.append_string_with_space(previous_proc_text,'- Patient has the following previous procedures reported:')
            for i in previous_proc_list:
                self.append_string_with_space(previous_proc_text,str(i))
            self.clinical_info_text.append("".join(previous_proc_text))
        if urgency == False:
            self.clinical_info_text.append('- Study was not an urgent request.')
        else:
            self.clinical_info_text.append('- Study was an URGENT request.')
        
        # Information regarding to why this patient could not go through automatic image analysis (acquisition limitaitions, previous procedures,...)
        limitations_list = [x for x in self.main_class.get_filtering()[1][self.ident]['Limitations'] if x is not False]
        
        image_text = []
        self.append_string_with_space(image_text,'Patient not suitable due to')
        if previous_proc_list != []:
            for i in previous_proc_list:
                self.append_string_with_space(image_text,i)
                if i == previous_proc_list[-1] and self.main_class.get_filtering()[1][self.ident]['Quality'] != 'Deficient' and limitations_list ==[]:
                    self.append_string_with_space(image_text,'.')
                else:
                    if self.main_class.get_filtering()[1][self.ident]['Quality'] == 'Deficient':
                        self.append_string_with_space(image_text,'deficient image quality')
                        if limitations_list != []:
                            for i in limitations_list:
                                if i == limitations_list[-1]:
                                    self.append_string_with_space(image_text,'and')
                                else:
                                    self.append_string_with_space(image_text,',')
                                self.append_string_with_space(image_text,i)
                                if i == limitations_list[-1]:
                                    self.append_string_with_space(image_text,'.')
                        else:
                            self.append_string_with_space(image_text,'.')
                    else:
                        for i in limitations_list:
                            if i == limitations_list[-1]:
                                self.append_string_with_space(image_text,'and')
                            else:
                                self.append_string_with_space(image_text,',')
                            self.append_string_with_space(image_text,i)
                            if i == limitations_list[-1]:
                                self.append_string_with_space(image_text,'.')
        else:
            if self.main_class.get_filtering()[1][self.ident]['Quality'] == 'Deficient':
                self.append_string_with_space(image_text,'deficient image quality')
                if limitations_list != []:
                    for i in limitations_list:
                        if i == limitations_list[-1]:
                            self.append_string_with_space(image_text,'and')
                        else:
                            self.append_string_with_space(image_text,',')
                        self.append_string_with_space(image_text,i)
                        if i == limitations_list[-1]:
                            self.append_string_with_space(image_text,'.')
                else:
                    self.append_string_with_space(image_text,'.')
            else:
                for i in limitations_list:
                    self.append_string_with_space(image_text,i)
                    if i == limitations_list[-1]:
                        self.append_string_with_space(image_text,'.')
                    else:
                        self.append_string_with_space(image_text,',')
        
        self.image_info_text.setPlainText("".join(image_text)) 
                        
        self.clinical_info_text.setEnabled(False)
        self.image_info_text.setEnabled(False)
    
    # method to join information for the report
    def append_string_with_space(self,list_of_strings,string):
        list_of_strings.append(string)
        list_of_strings.append(" ")


"""
CCTA VIEWER CODE:
    Method to show the Cardiac Imaging Expert reporting the CCTA a visual support so they can make corrections or report
    findings. This visual support is a mockup including a CCTA viewer in the three axes with a slider to go through the slices. 
    An option to overlap to this CCTA viewer the segmentation of the coronary arteries. It also includes a 3D reconstruction
    of the coronary tree segmented. Finally it includes the cMPRs of the coronary vessels. 
    This mockup is very limited and takes the data from already pre- and post-processed images from a public database.
    The cMPRs viewer consist of screenshots obtained from a CT analysis commercial software used in the hospital.
"""
# CCTA visualization (+ overlapping of coronary artery segmentation)
def read_img_nii(img_path):
    image_data = np.array(nib.load(img_path).get_fdata()) # read CCTA data
    return image_data

# set plotting window and slider
class ThreeDImageViewer(QMainWindow):
    def __init__(self, img_path, img_path_2):
        super().__init__()

        self.setWindowTitle("3D Image Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.canvas = MatplotlibCanvas(img_path, img_path_2)
        self.setCentralWidget(self.canvas)

        self.viewer_widget = QDockWidget("Image Viewer", self)
        self.viewer_widget.setWidget(ImageViewerWidget(self))
        self.addDockWidget(Qt.RightDockWidgetArea, self.viewer_widget)

# plotting of images by axes
class MatplotlibCanvas(FigureCanvas):
    def __init__(self, img_path, img_path_2):
        self.fig, self.axes = plt.subplots(2, 2) # Create a 2x2 grid of subplots
        self.img_data = read_img_nii(img_path)
        self.img_data_2 = read_img_nii(img_path_2)
        self.current_layer = [0, 0, 0]  # Initialize current layer for each view
        self.views = ['axial', 'coronal', 'sagittal'] # axes
        self.overlay = True  # Initialize with overlapped segmentation on

        super().__init__(self.fig)

        self.plot()

    # plot slices per axes
    def plot(self):
        for i, view in enumerate(self.views):
            if view == 'axial':
                array_view = np.rot90(self.img_data[:, :, self.current_layer[i]])
                self.axes[i, 0].imshow(array_view, cmap='gray')
                if self.overlay:
                    array_view_2 = np.rot90(self.img_data_2[:, :, self.current_layer[i]])
                    self.axes[i, 0].imshow(array_view_2, cmap='gray', alpha=0.2)
                self.axes[i, 0].set_title('Axial view', fontsize=10)
                self.axes[i, 0].axis('off')
            elif view == 'coronal':
                array_view = np.rot90(self.img_data[:, self.current_layer[i], :])
                self.axes[0, 1].imshow(array_view, cmap='gray')
                if self.overlay:
                    array_view_2 = np.rot90(self.img_data_2[:, self.current_layer[i], :])
                    self.axes[0, 1].imshow(array_view_2, cmap='gray', alpha=0.2)
                self.axes[0, 1].set_title('Coronal view', fontsize=10)
                self.axes[0, 1].axis('off')
            elif view == 'sagittal':
                array_view = np.rot90(self.img_data[self.current_layer[i], :, :])
                self.axes[1, 1].imshow(array_view, cmap='gray')
                if self.overlay:
                    array_view_2 = np.rot90(self.img_data_2[self.current_layer[i], :, :])
                    self.axes[1, 1].imshow(array_view_2, cmap='gray', alpha=0.2)
                self.axes[1, 1].set_title('Sagittal view', fontsize=10)
                self.axes[1, 1].axis('off')

        # Clear the subplot at position [1, 0]
        self.axes[1, 0].cla()
        self.axes[1, 0].axis('off')
        self.axes[1, 0].grid(False)

        self.draw()

    # update the plot when the slider has been moved
    def update_plot(self):
        self.fig.clf()  # Clear the figure
        self.axes = self.fig.subplots(2, 2) # Redefine subplots
        self.plot()

# viewer merging the slider and the matplotlib visualization
class ImageViewerWidget(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.layout = QVBoxLayout()

        self.slider = QSlider()
        self.slider.setMinimum(0)
        self.slider.setMaximum(511)  # Set maximum value for coronal and sagittal views (axial has less slices)
        self.slider.valueChanged.connect(self.slider_changed) # change slice with slider

        self.layout.addWidget(self.slider)
        
        # choice between only CCTA visualization or visualization of CCTA with the overlayed segmentation
        self.combo = QComboBox()
        self.combo.addItem("Overlayed segmentation") 
        self.combo.addItem("CCTA")
        self.combo.currentIndexChanged.connect(self.combo_changed)

        self.layout.addWidget(self.combo)
        self.setLayout(self.layout)
        
    # change slice of image depending on slider movement
    def slider_changed(self, value):
        for i in range(3):
            if self.parent.canvas.views[i] == 'axial':
                self.parent.canvas.current_layer[i] = min(value, 203)  # Limit the axial view slider to 203 (axial view has less slices than coronal and sagittal)
            else:
                self.parent.canvas.current_layer[i] = value
        self.parent.canvas.update_plot()

    # change visualization depending on overlay selected or not
    def combo_changed(self, index):
        if index == 0:
            self.parent.canvas.overlay = True
        else:
            self.parent.canvas.overlay = False
        self.parent.canvas.update_plot()

def run_viewer():
    # Access directory of the folder where the nifti images are
    _base_dir = os.getcwd()
    _images_dir = os.path.join(_base_dir, 'Case1_ASOCA', 'Test_nifti.nii')
    
    # Access all the elements in this folder
    list_of_images = os.listdir(_images_dir)
    img_path = '{}\\{}'.format(_images_dir, list_of_images[len(list_of_images)-1])
    
    _img_dir = os.path.join(_base_dir,'Normal_1_segmentation.nii')
    list_of_img = os.listdir(_img_dir)
    img_path_2 = '{}\\{}'.format(_img_dir, list_of_img[len(list_of_img)-1])
    
    window = ThreeDImageViewer(img_path, img_path_2)
    window.setGeometry(900,40,1000,650)
    window.show()

"""
REPORTING AND VALIDATION:
    Interface presenting the reporting clinician with the clinical and demographic information and CCTA findings (if applicable) 
    of the patient being reported. The reporting clinician can correct or introduce the image-related information.
"""
class ReportCoronaries(QMainWindow):
    def __init__(self,identifier,main_class):
        super().__init__()
        uic.loadUi('gui_report_coronaries3.ui',self)
        self.setWindowTitle('Reporting System')
        
        self.ident = identifier
        self.main_class = main_class 
        
        # set color for labels of plaque type
        self.fc_plaque.setStyleSheet("background-color: #fff959; color: black;")
        self.fl_plaque.setStyleSheet("background-color: #46ccfb; color: black;")
        self.vu_plaque.setStyleSheet("background-color: #ff2611; color: black;")
        self.stent.setStyleSheet("background-color: black; color: white;")
        
        # widget names for general info
        self.report_general = [self.FemaleSex,self.MaleSex,self.textAge,self.UrgentStudy,self.textPhysician,self.textHospital,self.textService,self.dateStudy,self.optionDominance,self.optionCACs]
        # names of the patient database for general info
        self.database_general = ['Sex','Age','Urgent study','Physician','Center','Service','Study date','Dominance','CACs']
        
        # widget names for segments' stenosis
        self.report_segments = [self.optionLCA,self.optionpLAD,self.optionmLAD,self.optiondLAD,self.optionD1,self.optionD2,self.optionpCx,self.optiondCx,self.optionOM1,self.optionOM2,self.optionLPD,self.optionLPL,self.optionRI,self.optionpRCA,self.optionmRCA,self.optiondRCA,self.optionRPD,self.optionRPL]
        # widget names for segments' plaque
        self.report_segments_plaque = [self.optionLCA_2,self.optionpLAD_2,self.optionmLAD_2,self.optiondLAD_2,self.optionD1_2,self.optionD2_2,self.optionpCx_2,self.optiondCx_2,self.optionOM1_2,self.optionOM2_2,self.optionLPD_2,self.optionLPL_2,self.optionRI_2,self.optionpRCA_2,self.optionmRCA_2,self.optiondRCA_2,self.optionRPD_2,self.optionRPL_2]
        # name of the patient database segments
        self.database_segments = ['LCA','p-LAD','m-LAD','d-LAD','D1','D2','p-Cx','d-Cx','OM1','OM2','LPD','LPL','RI','p-RCA','m-RCA','d-RCA','RPD','RPL']
        
        # types of dominances
        self.dominance_options = ['Right dominance','Left dominance','Codominance']
        
        # reported ranges of CACs
        self.CACs_options = [range(0,1),range(1,11),range(11,101),range(101,401),range(401,10000)]
        
        # reported stenosis ranges (in database)
        self.stenosis_options = ['0','1-24','25-49','50-69','70-99','100','ND']
        
        # reported CAD-RADS (in database)
        self.CADRADS_options = ['0','1','2','3','4A','4B','5','ND']        
        
        # reported plaque
        self.plaque_type = ['','Fibrocalcic','Fibrolipidic','Vulnerable','Stent']
        
        # indicate which information from the image, which in principle would have been acquired through some type of AI, is not acquired by any human
        self.AI_info_label.setStyleSheet("color: red;")
        ai_indicator = [self.as1,self.as2,self.as3,self.as4,self.as5,self.as6,self.as7,self.as8,self.as9,self.as10,self.as11,self.as12,self.as13,self.as14,self.as15,self.as16,self.as17,self.as18,self.as19,self.as20]
        for indicator in ai_indicator:
            indicator.setStyleSheet("color: red;")
        
        # Set the initial selection of the combo box based on the random variable
        self.set_combobox_selection()
        
        # call2action if some stenosis degree is changed
        for i in self.report_segments:
            i.currentIndexChanged.connect(self.changed_stenosis)
            i.currentIndexChanged.connect(lambda _, i=i: self.changed_index(i))
        
        # call2action if plaque is changed
        for i in self.report_segments_plaque:
            i.currentIndexChanged.connect(lambda _, i=i: self.changed_plaque(i))
        
        # call2action if dominance is changed
        self.optionDominance.currentIndexChanged.connect(lambda _, i=i: self.changed_index(self.optionDominance))
        self.previous_dominance = self.optionDominance.currentIndex()
        self.optionDominance.currentIndexChanged.connect(self.changed_dominance)
        
        # call2action if CACs is changed
        self.optionCACs.currentIndexChanged.connect(lambda _, i=i: self.changed_index(self.optionCACs)) 
        
        # validate the report
        self.ValidateReport.clicked.connect(self.validate_report)
        
        # open the visual support window
        self.VisualSupport.clicked.connect(self.visual_support)
        
    def set_combobox_selection(self):
        
        # patient going through automatic image analysis - insert information from the patient database to the interface for the clinician to correct
        if self.ident in self.main_class.get_imgAnalysis().keys():
            self.textID.setText(self.ident)
            self.textID.setEnabled(False)
            for i in range(len(self.database_general)):
                if i == 0:
                    sex = self.main_class.get_imgAnalysis()[self.ident]['EHR'][self.database_general[i]]
                    if sex == 'Female':
                        self.report_general[i].setChecked(True)
                    else:
                        self.report_general[i+1].setChecked(True)
                    self.report_general[i].setEnabled(False)
                    self.report_general[i+1].setEnabled(False)
                elif i==1:
                    self.report_general[i+1].setText(str(self.main_class.get_imgAnalysis()[self.ident]['EHR'][self.database_general[i]]))
                    self.report_general[i+1].setEnabled(False)
                elif i == 2:
                    if self.main_class.get_imgAnalysis()[self.ident]['EHR'][self.database_general[i]] == 'Yes':
                        self.report_general[i+1].setChecked(True)
                    self.report_general[i+1].setEnabled(False)
                elif i==3 or i==4 or i==5:
                    self.report_general[i+1].setText(str(self.main_class.get_imgAnalysis()[self.ident]['Admin'][self.database_general[i]]))
                    self.report_general[i+1].setEnabled(False)
                elif i == 6:
                    date = self.main_class.get_imgAnalysis()[self.ident]['Admin'][self.database_general[i]]
                    self.report_general[i+1].setDate(QDate(date.year, date.month, date.day))
                    self.report_general[i+1].setDisabled(True)
                else: 
                    if self.database_general[i] == 'Dominance':
                        self.report_general[i+1].setCurrentIndex(self.dominance_options.index(self.main_class.get_imgAnalysis()[self.ident][self.database_general[i]])+1)
                    else:
                        for j in range(len(self.CACs_options)):
                            if self.main_class.get_imgAnalysis()[self.ident][self.database_general[i]] in self.CACs_options[j]:
                                index_cacs = j+1
                        try:
                            self.report_general[i+1].setCurrentIndex(index_cacs)
                        except: 
                            self.report_general[i+1].setCurrentIndex(6)
            for i in range(len(self.database_segments)):
                for j in self.main_class.get_imgAnalysis()[self.ident]['Stenosis']:
                    if self.main_class.get_imgAnalysis()[self.ident]['Stenosis'][j][1] == self.database_segments[i]:
                        self.report_segments[i].setCurrentIndex(self.stenosis_options.index(self.main_class.get_imgAnalysis()[self.ident]['Stenosis'][j][0])+1)
                        break
                    elif j == sorted(self.main_class.get_imgAnalysis()[self.ident]['Stenosis'].keys())[-1]:
                        self.report_segments[i].setCurrentIndex(0)
                        self.report_segments[i].setStyleSheet("background-color: grey; color: white;")
                self.assign_color(self.report_segments[i])
                    
            CADRADS = ImageInfo_Generator().CADRADS_calculator_individual(self.main_class.get_imgAnalysis(),self.ident)[1]
            self.optionCADRADS.setCurrentIndex(self.CADRADS_options.index(CADRADS)+1)
            self.optionCADRADS.setEnabled(False)
                        
        # patient not going through automatic image analysis - insert information from the patient database so the clinician can make the report
        elif self.ident in self.main_class.get_filtering()[1].keys():
            self.textID.setText(self.ident)
            self.textID.setReadOnly(True)
            for i in range(len(self.database_general)):
                if i == 0:
                    sex = self.main_class.get_filtering()[1][self.ident]['EHR'][self.database_general[i]]
                    if sex == 'Female':
                        self.report_general[i].setChecked(True)
                    else:
                        self.report_general[i+1].setChecked(True)
                    self.report_general[i].setEnabled(False)
                    self.report_general[i+1].setEnabled(False)
                elif i == 1:
                    self.report_general[i+1].setText(str(self.main_class.get_filtering()[1][self.ident]['EHR'][self.database_general[i]]))
                    self.report_general[i+1].setReadOnly(True)
                elif i == 2:
                    if self.main_class.get_filtering()[1][self.ident]['EHR'][self.database_general[i]] == 'Yes':
                        self.report_general[i+1].setChecked(True)
                    self.report_general[i+1].setEnabled(False)
                elif i==3 or i==4 or i==5:
                    self.report_general[i+1].setText(str(self.main_class.get_filtering()[1][self.ident]['Admin'][self.database_general[i]]))
                    self.report_general[i+1].setReadOnly(True)
                elif i == 6:
                    date = self.main_class.get_filtering()[1][self.ident]['Admin'][self.database_general[i]]
                    self.report_general[i+1].setDate(QDate(date.year, date.month, date.day))
                    self.report_general[i+1].setDisabled(True)
            procedures = [x for x in self.main_class.get_filtering()[1][self.ident]['EHR']['Previous procedures'] if x is not False]
            if 'Stent/ACTP' in procedures and 'Coronary bypass' in procedures:
                self.optionS.setChecked(True)
                self.optionG.setChecked(True)
            elif 'Coronary bypass' in procedures:
                self.optionG.setChecked(True)
            elif 'Stent/ACTP' in procedures:
                self.optionS.setChecked(True)
            elif procedures != []:
                procedures2 = [k for k in procedures if (k != 'Stent/ACTP' and k != 'Coronary bypass')]
                self.textEdit.setText(f'Previous procedures: {procedures2}')
        else:
            print('ERROR')
    
    # if some of the stenosis of any segment is changed, correct CAD-RADS value
    def changed_stenosis(self):
        modified_stenosis = []
        for i in self.report_segments:
            modified_stenosis.append(i.currentText())
        if 'NEv' in modified_stenosis:
            CADRADS='N'
        elif '100%' in modified_stenosis: 
            CADRADS = '5'
        elif modified_stenosis[0]=='100%' or modified_stenosis[0]=='<99%' or modified_stenosis[0]=='<70%':
            CADRADS = '4B'
        elif modified_stenosis.count('<99%')>2:
            CADRADS = '4B'
        elif modified_stenosis.count('<99%')>0:
            CADRADS = '4A'
        elif modified_stenosis.count('<70%')>0:
            CADRADS = '3'
        elif modified_stenosis.count('<50%')>0:
            CADRADS = '2'
        elif modified_stenosis.count('<25%')>0:
            CADRADS = '1'
        else:
            CADRADS = '0'
        self.optionCADRADS.setCurrentIndex(self.CADRADS_options.index(CADRADS)+1)
    
    # assign color depending on the stenosis degree range
    def assign_color(self,combobox):
        if combobox.currentIndex() == 0:
            combobox.setStyleSheet("background-color: #4a4a4a; color: white;")
        elif combobox.currentIndex() == 1:
            combobox.setStyleSheet("background-color: #b5ebc7; color: black;")
        elif combobox.currentIndex() == 2:
            combobox.setStyleSheet("background-color: #fdd1cf; color: black;")
        elif combobox.currentIndex() == 3:
           combobox.setStyleSheet("background-color: #ffa39e; color: black;")
        elif combobox.currentIndex() == 4:
            combobox.setStyleSheet("background-color: #ff756e; color: black;")
        elif combobox.currentIndex() == 5:
            combobox.setStyleSheet("background-color: #f92611; color: black;")
        elif combobox.currentIndex() == 6:
            combobox.setStyleSheet("background-color: #8a0f03; color: white;")
        elif combobox.currentIndex() == 7:
            combobox.setStyleSheet("background-color: #4a4a4a; color: #a072fd; font-weight: bold")
    
    # if information marked as AI-obtained is modified by the doctor, this indicator will disapear
    def changed_index(self,combobox):
        segments = [self.as3,self.as4,self.as5,self.as6,self.as7,self.as8,self.as9,self.as10,self.as11,self.as12,self.as13,self.as14,self.as15,self.as16,self.as17,self.as18,self.as19,self.as20]
        if combobox == self.optionDominance: 
            self.as1.setText('')
        elif combobox == self.optionCACs:
            self.as2.setText('')
        else:
            segments[self.report_segments.index(combobox)].setText('')
            self.assign_color(combobox)
    
    # set color for each type of plaque
    def changed_color_plaque(self,combobox):
        if combobox.currentIndex() == 0:
            combobox.setStyleSheet("background-color: #4a4a4a; color: white;")
        elif combobox.currentIndex() == 1:
            combobox.setStyleSheet("background-color: #fff959; color: black;")
        elif combobox.currentIndex() == 2:
            combobox.setStyleSheet("background-color: #46ccfb; color: black;")
        elif combobox.currentIndex() == 3:
           combobox.setStyleSheet("background-color: #ff2611; color: black;")
        elif combobox.currentIndex() == 4:
            combobox.setStyleSheet("background-color: black; color: white;")
    
    # if plaque values are changed for some segments, the number of segments with plaque will be recalculated to correct the CAD-RADS modifier P
    # if some plaque type is vulnerable plaque or stent, the CAD-RADS modifiers HRP and/or S will be checked
    def changed_plaque(self,combobox):
        self.changed_color_plaque(combobox)
        stented = 0
        hrp = 0
        for i in self.report_segments_plaque:
            if i.currentIndex()==4:
                stented+=1
            if i.currentIndex()==3:
                hrp+=1
        if stented != 0:
            self.optionS.setChecked(True)
        else: 
            self.optionS.setChecked(False)
        if hrp != 0:
            self.optionHRP.setChecked(True)
        else: 
            self.optionHRP.setChecked(False)
        
        SIS = 0
        for i in self.report_segments_plaque:
            if i.currentIndex()!=0:
                SIS+=1
        if SIS == 0:
            self.optionPlaque.setCurrentIndex(0)
        elif SIS<3:
            self.optionPlaque.setCurrentIndex(1)
        elif SIS<5:
            self.optionPlaque.setCurrentIndex(2)
        elif SIS<8:
            self.optionPlaque.setCurrentIndex(3)
        else:
            self.optionPlaque.setCurrentIndex(4)
                
    # changed dominance will determine which vessels have to be reported (e.g., going from right to left dominance will eliminate vessels RPL and RPD and add LPL and LPD)
    def changed_dominance(self):
        prev = self.previous_dominance
        current = self.optionDominance.currentIndex()
        #Case right to left
        if prev == 1 and current == 2:
            self.optionRPD.setCurrentIndex(0)
            self.optionRPL.setCurrentIndex(0)
            self.optionRPD.setStyleSheet("background-color: grey; color: white;")
            self.optionRPL.setStyleSheet("background-color: grey; color: white;")
            self.optionLPD.setCurrentIndex(0)
            self.optionLPL.setCurrentIndex(0)
            self.optionLPD.setStyleSheet("background-color: white; color: black;")
            self.optionLPL.setStyleSheet("background-color: white; color: black;")
            self.previous_dominance = current
        
        #Case left to right
        elif prev == 2 and current == 1:
            self.optionRPD.setCurrentIndex(0)
            self.optionRPL.setCurrentIndex(0)
            self.optionRPD.setStyleSheet("background-color: white; color: black;")
            self.optionRPL.setStyleSheet("background-color: white; color: black;")
            self.optionLPD.setCurrentIndex(0)
            self.optionLPL.setCurrentIndex(0)
            self.optionLPD.setStyleSheet("background-color: grey; color: white;")
            self.optionLPL.setStyleSheet("background-color: grey; color: white;")
            self.previous_dominance = current
        
        #Case right to codominant   
        elif prev == 1 and current == 3:
            self.optionLPD.setCurrentIndex(0)
            self.optionLPL.setCurrentIndex(0)
            self.optionLPD.setStyleSheet("background-color: white; color: black;")
            self.optionLPL.setStyleSheet("background-color: white; color: black;")
            self.previous_dominance = current
        
        #Case left to codominant
        elif prev == 2 and current == 3:
            self.optionRPD.setCurrentIndex(0)
            self.optionRPL.setCurrentIndex(0)
            self.optionRPD.setStyleSheet("background-color: white; color: black;")
            self.optionRPL.setStyleSheet("background-color: white; color: black;")
            self.previous_dominance = current
        
        #Case codominant to right
        elif prev == 3 and current == 1:
            self.optionLPD.setCurrentIndex(0)
            self.optionLPL.setCurrentIndex(0)
            self.optionLPD.setStyleSheet("background-color: grey; color: white;")
            self.optionLPL.setStyleSheet("background-color: grey; color: white;")
            self.previous_dominance = current
            
        #Case codominant to left
        elif prev == 3 and current == 2:
            self.optionRPD.setCurrentIndex(0)
            self.optionRPL.setCurrentIndex(0)
            self.optionRPD.setStyleSheet("background-color: grey; color: white;")
            self.optionRPL.setStyleSheet("background-color: grey; color: white;")
            self.previous_dominance = current
    
    # open the validated report window
    def validate_report(self):
        # Close the current window
        self.close()
        # Generate a new window
        global final_report
        final_report = FinalReport(self)
        final_report.setGeometry(0,0,1250,900)
        final_report.show()
    
    # open the visual support window
    def visual_support(self):
        # run the CCTA viewer
        try: 
            run_viewer()
        except:
            pass
        
        # run the 3d reconstruction of the segmentation of the coronary tree and the cMPRs of the coronary vessels
        try: 
            directory = os.getcwd()
            stl_path = os.path.join(directory, 'Case1_ASOCA','Normal_1.stl')
            
            global cpr_view
            cpr_view = CPR_Viewer(self)
            cpr_view.setGeometry(600,700,1200,300)
            cpr_view.show()
        except: 
            pass
        
        # make that this 3d reconstruction can be seen in 3d and can be moved and rotated for easier visualization
        try: 
            mesh = o3d.io.read_triangle_mesh(stl_path)
            mesh = mesh.compute_vertex_normals()
            o3d.visualization.draw_geometries([mesh], window_name="Segementation View", left=550, top=80, width=500, height=500)
        except: 
            pass
"""
CPR viewer window: 
    Mockup of the visualization of the curved multi-planar reconstructions of the coronary arteries. This mockup is done by 
    using screenshoots of the cMPRs extracted from the CT analysis software used in the hospital.
"""
class CPR_Viewer(QMainWindow):
    def __init__(self,parent):
        super().__init__(parent)
        uic.loadUi('gui_CPRviewer.ui',self)
        self.setWindowTitle("Curved Planar Reformation (CPR) Viewer")
        
        self.selector.currentIndexChanged.connect(self.changed_vessel) # vessel selected in the list
        self.parent = parent
        
    def changed_vessel(self):
        vessel_name = self.selector.currentText() # vessel selected
        
        # for vessels which have more than one segment we take the maximum stenosis degree of all segments and select a screenshot with this stenosis degree range
        if vessel_name == 'LAD':
            LAD_aff = []
            LAD_v = [self.parent.optionpLAD,self.parent.optionmLAD,self.parent.optiondLAD]
            for v in LAD_v:
                LAD_aff.append(v.currentIndex())
            try:
                LAD_aff.pop(7)
            except:
                pass
            vessel_affectation = max(LAD_aff)
        elif vessel_name == 'Cx':
            Cx_aff = []
            Cx_v = [self.parent.optionpCx,self.parent.optiondCx]
            for v in Cx_v:
                Cx_aff.append(v.currentIndex())
            try:
                Cx_aff.pop(7)
            except:
                pass
            vessel_affectation = max(Cx_aff)
        elif vessel_name == 'RCA':
            RCA_aff = []
            RCA_v = [self.parent.optionpRCA,self.parent.optionmRCA,self.parent.optiondRCA]
            for v in RCA_v:
                RCA_aff.append(v.currentIndex())
            try:
                RCA_aff.pop(7)
            except:
                pass
            vessel_affectation = max(RCA_aff)
        else:      
            vessel_affectation = self.parent.report_segments[self.parent.database_segments.index(vessel_name)].currentIndex()
        
        if vessel_affectation == 1:
            vessel = 'noCAD'
        elif vessel_affectation == 2:
            vessel = 'minimalCAD'
        elif vessel_affectation == 3:
            vessel = 'mildCAD'
        elif vessel_affectation == 4:
            vessel = 'moderateCAD'
        elif vessel_affectation == 5:
            vessel = 'severeCAD'
        elif vessel_affectation == 6:
            vessel = 'obstructiveCAD'
        else:
            vessel = ''
        
        # cMPRs are shown based on the stenosis degree range of the reported vessel and not by the vessel per se.
        # if a vessel has a minimal CAD, the screenshot of the cMPRs showing a minimal CAD will be plotted.
        
        if vessel != '':
            try: 
                directory = os.getcwd()
                
                # Attention!!! If original images are not available but you want to test this part of the code,
                # try to get screenshoots of cMPRs of coronary vessels and save them in the same directory of this code.
                # Inside this directory, a folder called 'CPR' must be created where this screenshoots will be saved.
                # Each screenshot must be saved with the degree of CAD. (e.g. 'moderateCAD.png', 'mildCAD.png',...).
                cpr_path = os.path.join(directory, 'CPR',vessel)
                
                cpr_image = cpr_path+'.png'
                pixmap = QPixmap(cpr_image)
                self.CPR.setPixmap(pixmap)
            except: 
                pass
        else:
            pixmap = QPixmap()
            self.CPR.setPixmap(pixmap)
        
"""
FINAL REPORT VISUALIZATION: 
    Visualization of the information of the case report validated by the Cardiac Imaging Expert (reporting clinician). 
    This information is only for consultation, it cannot be modified. From this, a RIS report can be extracted.
"""
class FinalReport(QMainWindow):
    def __init__(self,parent):
        super().__init__()
        uic.loadUi('gui_FINALreport_coronaries3.ui',self)
        self.setWindowTitle('Final Report')
        self.parent = parent
        self.ident = self.parent.ident
        self.main_class = self.parent.main_class
        
        # gathering all the patient information from the reporting system 
        self.textID.setText(self.parent.textID.text())
        self.textID.setEnabled(False)
        self.textAge.setText(self.parent.textAge.text())
        self.textAge.setEnabled(False)
        self.FemaleSex.setChecked(self.parent.FemaleSex.isChecked())
        self.FemaleSex.setEnabled(False)
        self.MaleSex.setChecked(self.parent.MaleSex.isChecked())
        self.MaleSex.setEnabled(False)
        self.UrgentStudy.setChecked(self.parent.UrgentStudy.isChecked())
        self.UrgentStudy.setEnabled(False)
        self.textPhysician.setText(self.parent.textPhysician.text())
        self.textPhysician.setEnabled(False)
        self.textHospital.setText(self.parent.textHospital.text())
        self.textHospital.setEnabled(False)
        self.textService.setText(self.parent.textService.text())
        self.textService.setEnabled(False)
        self.dateStudy.setDate(self.parent.dateStudy.date())
        self.dateStudy.setDisabled(True)
        self.optionDominance.setCurrentIndex(self.parent.optionDominance.currentIndex())
        self.optionDominance.setEnabled(False)
        self.optionCACs.setCurrentIndex(self.parent.optionCACs.currentIndex())
        self.optionCACs.setEnabled(False)
        
        # gathering information regarding the vessels stenosis degree and plaque type
        self.optionLCA.setCurrentIndex(self.parent.optionLCA.currentIndex())
        self.optionLCA.setEnabled(False)
        self.optionLCA_2.setCurrentIndex(self.parent.optionLCA_2.currentIndex())
        self.optionLCA_2.setEnabled(False)
        
        self.optionpLAD.setCurrentIndex(self.parent.optionpLAD.currentIndex())
        self.optionpLAD.setEnabled(False)
        self.optionpLAD_2.setCurrentIndex(self.parent.optionpLAD_2.currentIndex())
        self.optionpLAD_2.setEnabled(False)
        
        self.optionmLAD.setCurrentIndex(self.parent.optionmLAD.currentIndex())
        self.optionmLAD.setEnabled(False)
        self.optionmLAD_2.setCurrentIndex(self.parent.optionmLAD_2.currentIndex())
        self.optionmLAD_2.setEnabled(False)
        
        self.optiondLAD.setCurrentIndex(self.parent.optiondLAD.currentIndex())
        self.optiondLAD.setEnabled(False)
        self.optiondLAD_2.setCurrentIndex(self.parent.optiondLAD_2.currentIndex())
        self.optiondLAD_2.setEnabled(False)
        
        self.optionD1.setCurrentIndex(self.parent.optionD1.currentIndex())
        self.optionD1.setEnabled(False)
        self.optionD1_2.setCurrentIndex(self.parent.optionD1_2.currentIndex())
        self.optionD1_2.setEnabled(False)
        
        self.optionD2.setCurrentIndex(self.parent.optionD2.currentIndex())
        self.optionD2.setEnabled(False)
        self.optionD2_2.setCurrentIndex(self.parent.optionD2_2.currentIndex())
        self.optionD2_2.setEnabled(False)
        
        self.optionpCx.setCurrentIndex(self.parent.optionpCx.currentIndex())
        self.optionpCx.setEnabled(False)
        self.optionpCx_2.setCurrentIndex(self.parent.optionpCx_2.currentIndex())
        self.optionpCx_2.setEnabled(False)
        
        self.optiondCx.setCurrentIndex(self.parent.optiondCx.currentIndex())
        self.optiondCx.setEnabled(False)
        self.optiondCx_2.setCurrentIndex(self.parent.optiondCx_2.currentIndex())
        self.optiondCx_2.setEnabled(False)
        
        self.optionOM1.setCurrentIndex(self.parent.optionOM1.currentIndex())
        self.optionOM1.setEnabled(False)
        self.optionOM1_2.setCurrentIndex(self.parent.optionOM1_2.currentIndex())
        self.optionOM1_2.setEnabled(False)
        
        self.optionOM2.setCurrentIndex(self.parent.optionOM2.currentIndex())
        self.optionOM2.setEnabled(False)
        self.optionOM2_2.setCurrentIndex(self.parent.optionOM2_2.currentIndex())
        self.optionOM2_2.setEnabled(False)
        
        self.optionLPD.setCurrentIndex(self.parent.optionLPD.currentIndex())
        self.optionLPD.setEnabled(False)
        self.optionLPD_2.setCurrentIndex(self.parent.optionLPD_2.currentIndex())
        self.optionLPD_2.setEnabled(False)
        
        self.optionLPL.setCurrentIndex(self.parent.optionLPL.currentIndex())
        self.optionLPL.setEnabled(False)
        self.optionLPL_2.setCurrentIndex(self.parent.optionLPL_2.currentIndex())
        self.optionLPL_2.setEnabled(False)
        
        self.optionRI.setCurrentIndex(self.parent.optionRI.currentIndex())
        self.optionRI.setEnabled(False)
        self.optionRI_2.setCurrentIndex(self.parent.optionRI_2.currentIndex())
        self.optionRI_2.setEnabled(False)
        
        self.optionpRCA.setCurrentIndex(self.parent.optionpRCA.currentIndex())
        self.optionpRCA.setEnabled(False)
        self.optionpRCA_2.setCurrentIndex(self.parent.optionpRCA_2.currentIndex())
        self.optionpRCA_2.setEnabled(False)
        
        self.optionmRCA.setCurrentIndex(self.parent.optionmRCA.currentIndex())
        self.optionmRCA.setEnabled(False)
        self.optionmRCA_2.setCurrentIndex(self.parent.optionmRCA_2.currentIndex())
        self.optionmRCA_2.setEnabled(False)
        
        self.optiondRCA.setCurrentIndex(self.parent.optiondRCA.currentIndex())
        self.optiondRCA.setEnabled(False)
        self.optiondRCA.setCurrentIndex(self.parent.optiondRCA.currentIndex())
        self.optiondRCA.setEnabled(False)
        
        self.optionRPD.setCurrentIndex(self.parent.optionRPD.currentIndex())
        self.optionRPD.setEnabled(False)
        self.optionRPD_2.setCurrentIndex(self.parent.optionRPD_2.currentIndex())
        self.optionRPD_2.setEnabled(False)
        
        self.optionRPL.setCurrentIndex(self.parent.optionRPL.currentIndex())
        self.optionRPL.setEnabled(False)
        self.optionRPL_2.setCurrentIndex(self.parent.optionRPL_2.currentIndex())
        self.optionRPL_2.setEnabled(False)
        
        # gathering other image-related information
        self.optionCADRADS.setCurrentIndex(self.parent.optionCADRADS.currentIndex())
        self.optionCADRADS.setEnabled(False)
        self.optionPlaque.setCurrentIndex(self.parent.optionPlaque.currentIndex())
        self.optionPlaque.setEnabled(False)
        self.optionN.setChecked(self.parent.optionN.isChecked())
        self.optionN.setEnabled(False)
        self.optionHRP.setChecked(self.parent.optionHRP.isChecked())
        self.optionHRP.setEnabled(False)
        self.optionIschemia.setCurrentIndex(self.parent.optionIschemia.currentIndex())
        self.optionIschemia.setEnabled(False)
        self.optionS.setChecked(self.parent.optionS.isChecked())
        self.optionS.setEnabled(False)
        self.optionG.setChecked(self.parent.optionG.isChecked())
        self.optionG.setEnabled(False)
        self.optionE.setChecked(self.parent.optionE.isChecked())
        self.optionE.setEnabled(False)
        self.textEdit.setText(self.parent.textEdit.toPlainText())
        self.textEdit.setEnabled(False)
        
        # set color to the plaque type labels
        self.fc_plaque.setStyleSheet("background-color: #fff959; color: black;")
        self.fl_plaque.setStyleSheet("background-color: #46ccfb; color: black;")
        self.vu_plaque.setStyleSheet("background-color: #ff2611; color: black;")
        self.stent.setStyleSheet("background-color: black; color: white;")
        
        # name of the reported vessels widgets
        self.reported_vessels = [self.optionLCA,self.optionpLAD,self.optionmLAD,self.optiondLAD,self.optionpCx,self.optiondCx,self.optionD1,self.optionD2,self.optionOM1,self.optionOM2,self.optionLPD,self.optionLPL,self.optionRI,self.optionpRCA,self.optionmRCA,self.optiondRCA,self.optionRPD,self.optionRPL]
        
        # name of the segments of the vessels 
        self.name_vessels = ['LCA','p-LAD','m-LAD','d-LAD','p-Cx','d-Cx','D1','D2','OM1','OM2','LPD','LPL','RI','p-RCA','m-RCA','d-RCA','RPD','RPL']
        
        # name of the widgets for plaque 
        self.report_segments_plaque = [self.optionLCA_2,self.optionpLAD_2,self.optionmLAD_2,self.optiondLAD_2,self.optionD1_2,self.optionD2_2,self.optionpCx_2,self.optiondCx_2,self.optionOM1_2,self.optionOM2_2,self.optionLPD_2,self.optionLPL_2,self.optionRI_2,self.optionpRCA_2,self.optionmRCA_2,self.optiondRCA_2,self.optionRPD_2,self.optionRPL_2]
        
        # assign color for stenosis degree ranges
        for vessel in self.reported_vessels:
            self.parent.assign_color(vessel)
            
        # assign color for types of plaques
        for vessel in self.report_segments_plaque:
            self.parent.changed_color_plaque(vessel)
        
        # types of stenosis degree reported in the reporting system
        self.reported_degree = ['','0%','<25%','<50%','<70%','<99%','100%','NEv']
        # types of stenosis degree reported in the patient database 
        self.degree = ['NA','0','1-24','25-49','50-69','70-99','100','ND']
        
        # type of calcium scores reported in the reporting system
        self.calcium = ['','0','1-10','11-100','101-400','>400','NA']
        
        # type of plaques reported in the reporting system
        self.plaque_type = ['','Fibrocalcic','Fibrolipidic','Vulnerable','Stent']
        
        # update the validated patient information into the patient database
        self.update_records()
        self.pushButton_3.clicked.connect(self.report_button) # generate RIS report
    
    
    # for the reported patient, take the new information and change it in the patient database
    def update_records(self):
        #UPDATE AI REPORTS
        if self.ident in self.main_class.get_imgAnalysis().keys():
            stenosis_degree_reported = []
            for j in self.main_class.get_imgAnalysis()[self.ident]['Stenosis']:
                stenosis_degree_reported.append(self.main_class.get_imgAnalysis()[self.ident]['Stenosis'][j][1])
                index_name = self.name_vessels.index(self.main_class.get_imgAnalysis()[self.ident]['Stenosis'][j][1])
                self.main_class.get_imgAnalysis()[self.ident]['Stenosis'][j][0] = self.degree[self.reported_vessels[index_name].currentIndex()]
                
            stenosis_degree_unreported = [x for x in self.name_vessels if x not in stenosis_degree_reported]
                        
            counter = 1
            for i in range(len(stenosis_degree_unreported)):
                index_name = self.name_vessels.index(stenosis_degree_unreported[i])
                if self.reported_vessels[index_name].currentIndex() != 0:
                    self.main_class.get_imgAnalysis()[self.ident]['Stenosis'][int(j)+counter]=[self.degree[self.reported_vessels[index_name].currentIndex()],stenosis_degree_unreported[i]]
                    counter += 1
                    
            self.main_class.get_imgAnalysis()[self.ident]['Plaque segments'] = {}
            for i in range(len(self.report_segments_plaque)):
                self.main_class.get_imgAnalysis()[self.ident]['Plaque segments'][i]=[self.report_segments_plaque[i].currentText(),self.name_vessels[i]]
            
            self.main_class.get_imgAnalysis()[self.ident]['CACs']=self.calcium[self.optionCACs.currentIndex()]
            self.main_class.get_imgAnalysis()[self.ident]['Dominance']=self.optionDominance.currentText()
            if self.optionCADRADS.currentText()[:1] == '4':
                self.main_class.get_imgAnalysis()[self.ident]['CADRADS']=self.optionCADRADS.currentText()[:2]
            elif self.optionCADRADS.currentText()[:1] == 'N':
                self.main_class.get_imgAnalysis()[self.ident]['CADRADS']='ND'
            else:
                self.main_class.get_imgAnalysis()[self.ident]['CADRADS']=self.optionCADRADS.currentText()[:1]
            self.main_class.get_imgAnalysis()[self.ident]['Plaque']=self.optionPlaque.currentText()
            self.main_class.get_imgAnalysis()[self.ident]['Non-diagnostic']=True if self.optionN.isChecked() else False
            self.main_class.get_imgAnalysis()[self.ident]['HRP']=True if self.optionHRP.isChecked() else False
            self.main_class.get_imgAnalysis()[self.ident]['Stent']=True if self.optionS.isChecked() else False
            self.main_class.get_imgAnalysis()[self.ident]['Graft']=True if self.optionG.isChecked() else False
            self.main_class.get_imgAnalysis()[self.ident]['Exceptions']=True if self.optionE.isChecked() else False
            self.main_class.get_imgAnalysis()[self.ident]['Ischemia']=self.optionIschemia.currentText()
            self.main_class.get_imgAnalysis()[self.ident]['Additional comments']=self.textEdit.toPlainText()
          
        #UPDATE NON-AI REPORTS
        elif self.ident in self.main_class.get_filtering()[1].keys():
            self.main_class.get_filtering()[1][self.ident]['Stenosis'] = {}
            for i in range(len(self.reported_vessels)):
                if self.reported_degree.index(self.reported_vessels[i].currentIndex())!=0:
                    index = self.reported_degree.index(self.reported_vessels[i].currentText())
                    self.main_class.get_filtering()[1][self.ident]['Stenosis'][i]=[self.degree[index],self.name_vessels[i]]
                
            self.main_class.get_filtering()[1][self.ident]['Plaque segments'] = {}
            for i in range(len(self.report_segments_plaque)):
                self.main_class.get_filtering()[1][self.ident]['Plaque segments'][i]=[self.report_segments_plaque[i].currentText(),self.name_vessels[i]]
            
            self.main_class.get_filtering()[1][self.ident]['CACs']=self.calcium[self.optionCACs.currentIndex()]
            self.main_class.get_filtering()[1][self.ident]['Dominance']=self.optionDominance.currentText()
            if self.optionCADRADS.currentText()[:1] == '4':
               self.main_class.get_filtering()[1][self.ident]['CADRADS']=self.optionCADRADS.currentText()[:2]
            elif self.optionCADRADS.currentText()[:1] == 'N':
                self.main_class.get_filtering()[1][self.ident]['CADRADS']='ND'
            else:
                self.main_class.get_filtering()[1][self.ident]['CADRADS']=self.optionCADRADS.currentText()[:1]
            self.main_class.get_filtering()[1][self.ident]['Plaque']=self.optionPlaque.currentText()
            self.main_class.get_filtering()[1][self.ident]['Non-diagnostic']=True if self.optionN.isChecked() else False
            self.main_class.get_filtering()[1][self.ident]['HRP']=True if self.optionHRP.isChecked() else False
            self.main_class.get_filtering()[1][self.ident]['Stent']=True if self.optionS.isChecked() else False
            self.main_class.get_filtering()[1][self.ident]['Graft']=True if self.optionG.isChecked() else False
            self.main_class.get_filtering()[1][self.ident]['Exceptions']=True if self.optionE.isChecked() else False
            self.main_class.get_filtering()[1][self.ident]['Ischemia']=self.optionIschemia.currentText()
            self.main_class.get_filtering()[1][self.ident]['Additional comments']=self.textEdit.toPlainText()
      
    # generate a RIS report from these findings
    def report_button(self):
        self.main_class.set_reportGeneration(self.main_class.get_imgAnalysis(),self.ident)
        report = self.main_class.get_reportGeneration()
        global reportRIS
        reportRIS = report_RIS(self,report)
        reportRIS.show()
        
"""
WRITTEN REPORT FOR RIS UPLOAD: Generation of a written report from the validated information from the reporting system.
"""
class report_RIS(QMainWindow):
    def __init__(self,parent,report):
        super().__init__()
        uic.loadUi('gui_report_RIS.ui',self)
        self.setWindowTitle('RIS report')
        self.parent = parent
        
        # acquire information from the reporting system
        # vessels information (stenosis degree and plaque)
        self.optionLCA.setCurrentIndex(self.parent.optionLCA.currentIndex())
        self.optionLCA.setEnabled(False)
        self.optionLCA_2.setCurrentIndex(self.parent.optionLCA_2.currentIndex())
        self.optionLCA_2.setEnabled(False)
        
        self.optionpLAD.setCurrentIndex(self.parent.optionpLAD.currentIndex())
        self.optionpLAD.setEnabled(False)
        self.optionpLAD_2.setCurrentIndex(self.parent.optionpLAD_2.currentIndex())
        self.optionpLAD_2.setEnabled(False)
        
        self.optionmLAD.setCurrentIndex(self.parent.optionmLAD.currentIndex())
        self.optionmLAD.setEnabled(False)
        self.optionmLAD_2.setCurrentIndex(self.parent.optionmLAD_2.currentIndex())
        self.optionmLAD_2.setEnabled(False)
        
        self.optiondLAD.setCurrentIndex(self.parent.optiondLAD.currentIndex())
        self.optiondLAD.setEnabled(False)
        self.optiondLAD_2.setCurrentIndex(self.parent.optiondLAD_2.currentIndex())
        self.optiondLAD_2.setEnabled(False)
        
        self.optionD1.setCurrentIndex(self.parent.optionD1.currentIndex())
        self.optionD1.setEnabled(False)
        self.optionD1_2.setCurrentIndex(self.parent.optionD1_2.currentIndex())
        self.optionD1_2.setEnabled(False)
        
        self.optionD2.setCurrentIndex(self.parent.optionD2.currentIndex())
        self.optionD2.setEnabled(False)
        self.optionD2_2.setCurrentIndex(self.parent.optionD2_2.currentIndex())
        self.optionD2_2.setEnabled(False)
        
        self.optionpCx.setCurrentIndex(self.parent.optionpCx.currentIndex())
        self.optionpCx.setEnabled(False)
        self.optionpCx_2.setCurrentIndex(self.parent.optionpCx_2.currentIndex())
        self.optionpCx_2.setEnabled(False)
        
        self.optiondCx.setCurrentIndex(self.parent.optiondCx.currentIndex())
        self.optiondCx.setEnabled(False)
        self.optiondCx_2.setCurrentIndex(self.parent.optiondCx_2.currentIndex())
        self.optiondCx_2.setEnabled(False)
        
        self.optionOM1.setCurrentIndex(self.parent.optionOM1.currentIndex())
        self.optionOM1.setEnabled(False)
        self.optionOM1_2.setCurrentIndex(self.parent.optionOM1_2.currentIndex())
        self.optionOM1_2.setEnabled(False)
        
        self.optionOM2.setCurrentIndex(self.parent.optionOM2.currentIndex())
        self.optionOM2.setEnabled(False)
        self.optionOM2_2.setCurrentIndex(self.parent.optionOM2_2.currentIndex())
        self.optionOM2_2.setEnabled(False)
        
        self.optionLPD.setCurrentIndex(self.parent.optionLPD.currentIndex())
        self.optionLPD.setEnabled(False)
        self.optionLPD_2.setCurrentIndex(self.parent.optionLPD_2.currentIndex())
        self.optionLPD_2.setEnabled(False)
        
        self.optionLPL.setCurrentIndex(self.parent.optionLPL.currentIndex())
        self.optionLPL.setEnabled(False)
        self.optionLPL_2.setCurrentIndex(self.parent.optionLPL_2.currentIndex())
        self.optionLPL_2.setEnabled(False)
        
        self.optionRI.setCurrentIndex(self.parent.optionRI.currentIndex())
        self.optionRI.setEnabled(False)
        self.optionRI_2.setCurrentIndex(self.parent.optionRI_2.currentIndex())
        self.optionRI_2.setEnabled(False)
        
        self.optionpRCA.setCurrentIndex(self.parent.optionpRCA.currentIndex())
        self.optionpRCA.setEnabled(False)
        self.optionpRCA_2.setCurrentIndex(self.parent.optionpRCA_2.currentIndex())
        self.optionpRCA_2.setEnabled(False)
        
        self.optionmRCA.setCurrentIndex(self.parent.optionmRCA.currentIndex())
        self.optionmRCA.setEnabled(False)
        self.optionmRCA_2.setCurrentIndex(self.parent.optionmRCA_2.currentIndex())
        self.optionmRCA_2.setEnabled(False)
        
        self.optiondRCA.setCurrentIndex(self.parent.optiondRCA.currentIndex())
        self.optiondRCA.setEnabled(False)
        self.optiondRCA.setCurrentIndex(self.parent.optiondRCA.currentIndex())
        self.optiondRCA.setEnabled(False)
        
        self.optionRPD.setCurrentIndex(self.parent.optionRPD.currentIndex())
        self.optionRPD.setEnabled(False)
        self.optionRPD_2.setCurrentIndex(self.parent.optionRPD_2.currentIndex())
        self.optionRPD_2.setEnabled(False)
        
        self.optionRPL.setCurrentIndex(self.parent.optionRPL.currentIndex())
        self.optionRPL.setEnabled(False)
        self.optionRPL_2.setCurrentIndex(self.parent.optionRPL_2.currentIndex())
        self.optionRPL_2.setEnabled(False)
        
        # name of reported vessels for stenosis degree
        self.reported_vessels = [self.optionLCA,self.optionpLAD,self.optionmLAD,self.optiondLAD,self.optionpCx,self.optiondCx,self.optionD1,self.optionD2,self.optionOM1,self.optionOM2,self.optionLPD,self.optionLPL,self.optionRI,self.optionpRCA,self.optionmRCA,self.optiondRCA,self.optionRPD,self.optionRPL]
        
        # name of reported vessels for plaque type
        self.report_segments_plaque = [self.optionLCA_2,self.optionpLAD_2,self.optionmLAD_2,self.optiondLAD_2,self.optionD1_2,self.optionD2_2,self.optionpCx_2,self.optiondCx_2,self.optionOM1_2,self.optionOM2_2,self.optionLPD_2,self.optionLPL_2,self.optionRI_2,self.optionpRCA_2,self.optionmRCA_2,self.optiondRCA_2,self.optionRPD_2,self.optionRPL_2]
        
        # set types of plaque colors for labels
        self.fc_plaque.setStyleSheet("background-color: #fff959; color: black;")
        self.fl_plaque.setStyleSheet("background-color: #46ccfb; color: black;")
        self.vu_plaque.setStyleSheet("background-color: #ff2611; color: black;")
        self.stent.setStyleSheet("background-color: black; color: white;")
        
        # set color for stenosis degree ranges
        for vessel in self.reported_vessels:
            self.parent.parent.assign_color(vessel)
        
        # set color for type of plaque
        for vessel in self.report_segments_plaque:
            self.parent.parent.changed_color_plaque(vessel)
        
        # report generation 
        self.report = report
        self.strings = []
        for string in self.report:
            self.append_string_with_space(string)
                
        # Join the strings with space and set them to the text edit
        self.Report.setPlainText("".join(self.strings))   
        self.save.clicked.connect(self.save_text)
    
    # method to join information with a new line
    def append_string_with_newline(self,string):
        # Append string to the list with a new line
        self.strings.append(string)
        self.strings.append("\n")
    
    # method to join information with a space
    def append_string_with_space(self,string):
        self.strings.append(string)
        self.strings.append(" ")
    
    # save RIS report to computer
    def save_text(self):
        text = self.Report.toPlainText()

        # Open a file dialog to select the file to save
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt)")

        # If a file was selected, save the text to the file
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(text)
                QMessageBox.information(self, "File Saved", "The file has been saved successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
                
# run code                   
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = LogIn()
    GUI.show()
    sys.exit(app.exec_())