# -*- coding: utf-8 -*-
"""
Created on Fri May 24 17:48:44 2024

@author: ferbe
"""
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 18:40:34 2024

@author: ferbe
"""
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
BASELINE CODE: Database
"""
class main:
    def __init__(self,num_patients=15):
        self.initial_patients = Initial_Patient_Generation(num_patients).generate_initial_pool()
        
        self.set_order4image(self.initial_patients)
        self.set_imageAcquisition(self.initial_patients,self.get_order4image())
        self.set_filtering(self.get_imageAcquisition())
        self.set_imgAnalysis(self.get_filtering()[0])
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
        analysed_patient_images = ImageInfo_Generator().image_data_generator(dic)
        analysed_patient_images = PreTestScore().assign_risk(analysed_patient_images)
        analysed_patient_images = ImageInfo_Generator().CADRADS_calculator(analysed_patient_images)
        self.__imgAnalysis = analysed_patient_images
    def get_imgAnalysis(self):
        return self.__imgAnalysis
    
    def set_order4validation(self,dic_AI,dic_notAI):
        self.__order4validation = Prioritization_Validation(dic_AI,dic_notAI).set_order()
    def get_order4validation(self):
        return self.__order4validation
        
    #def order4validation(self,dic_AI,dic_notAI):
    #    return Prioritization_Validation(dic_AI,dic_notAI).set_order()
    
    def set_reportGeneration(self,dic,identifier,option):
        self.__reportGeneration = Report_Generation().show_report(dic,identifier,option)
    def get_reportGeneration(self):
        return self.__reportGeneration
    
    order4image = property(get_order4image,set_order4image)
    imageAcquisition = property(get_imageAcquisition,set_imageAcquisition)
    filtering = property(get_filtering,set_filtering)
    imgAnalysis = property(get_imgAnalysis,set_imgAnalysis)
    order4validation = property(get_order4validation,set_order4validation)
    reportGeneration = property(get_reportGeneration,set_reportGeneration)

"""
LOGIN OF PHYSICIAN FOR REPORTING
"""
class LogIn(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('gui_login.ui', self)
        
        self.main_class = main()
        
        self.user.setPlaceholderText("Enter user here")
        self.user.textChanged.connect(self.check_enable_button)
        
        self.password.setPlaceholderText("Enter password here")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.textChanged.connect(self.check_enable_button)
        
        self.Enter.setEnabled(False)
        self.Enter.clicked.connect(self.check_dictionary)
        self.password.returnPressed.connect(self.check_dictionary)
        
        self.password_dic = {'test': ['password', ['generate', 'acquire', 'report']], 
                             'abdel': ['moustafa', ['generate', 'report']], 
                             'ruben': ['leta', ['generate', 'report']]}
    
    def check_enable_button(self):
        text1 = self.user.text().strip()
        text2 = self.password.text().strip()
        self.Enter.setEnabled(bool(text1 and text2))
    
    def check_permissions(self):
        user = self.user.text().strip()
        permissions = self.password_dic.get(user, [None, []])[1]
        return permissions
    
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
ACTIVITIES WINDOW
"""
class Activities (QMainWindow):
    def __init__(self,parent):
        super().__init__()
        uic.loadUi('gui_choose_action.ui',self)   
        self.setWindowTitle('Actions')
        self.parent = parent
        self.main_class = self.parent.main_class
        
        self.generate.clicked.connect(self.generate_checked)
        self.acquire.clicked.connect(self.acquire_checked)
        self.report.clicked.connect(self.report_checked)
        
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
HOME WINDOW
"""
class Home (QMainWindow):
    def __init__(self,parent):
        super().__init__()
        uic.loadUi('gui_Home.ui',self)   
        self.setWindowTitle('Home')
        self.parent = parent
        self.main_class = self.parent.main_class
        
        self.new_p.clicked.connect(self.new_patient)
        self.search_p.clicked.connect(self.search_patient)
    
    def new_patient(self):
        self.create_window = Register(self)
        self.create_window.show()
    
    def search_patient(self):
        self.search_window = Search(self)
        self.search_window.show()

"""
REGISTER NEW PATIENTS
"""
class Register(QMainWindow):
    def __init__(self,parent):
        super().__init__(parent)
        uic.loadUi('gui_report_clinical.ui',self)
        self.setWindowTitle('Register Patient')
        self.parent = parent
        self.main_class = self.parent.main_class
        self.ident = str(int(sorted(self.main_class.initial_patients.keys())[-1])+1)
        self.textID.setText(str(self.ident))
        self.textID.setEnabled(False)
        
        self.register_button.clicked.connect(self.registered_patient)
    
    def registered_patient(self):
        #try:
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
        print('NEW PATIENT: ',self.ident,self.main_class.initial_patients[self.ident])  
        #except:
         #   QMessageBox.warning(self,"Missing information",'There is missing information.')

"""
SEARCH PATIENT
"""
class Search(QMainWindow):
    def __init__(self,parent):
        super().__init__(parent)
        uic.loadUi('gui_report_clinical.ui',self)
        self.setWindowTitle('Search Patient')
        self.parent = parent
        self.main_class = self.parent.main_class
        
        self.textID.setStyleSheet("background-color: red; color: white; font-weight: bold")
        
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
        
        self.textID.textChanged.connect(self.get_id)
        self.register_button.setText('SEARCH')
        self.register_button.clicked.connect(self.search_patient)
        print('PACIENTES INICIALES: ',self.main_class.initial_patients)
    
    def get_id(self):
        self.ident = self.textID.text().strip()
    
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
            QMessageBox.warning(self,'Inexistent patient','There is no patient with this ID.')


"""
ORDERED CCTA ACQUISITION LIST
"""
class AcquisitionList (QMainWindow):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi('gui_acquisition_list.ui',self)
        self.setWindowTitle('CCTA Acquisition List')
        
        # Access the grid layout from the loaded UI
        self.grid_layout = self.gridLayout
        
        self.parent = parent
        self.main_class = self.parent.parent.main_class
        order = self.main_class.get_order4image()
        num_patients = len(order)
         
        for i in range(num_patients):
            #Add rows with labels and buttons based on the specified number input
            num_order = QLabel(f"{i+1}")
            num_order.setAlignment(QtCore.Qt.AlignCenter)
            ident = QLabel(order[i][0])
            ident.setAlignment(QtCore.Qt.AlignCenter)
            age = QLabel(str(order[i][1]))
            age.setAlignment(QtCore.Qt.AlignCenter)
            sex = QLabel(order[i][2])
            sex.setAlignment(QtCore.Qt.AlignCenter)
            chest_pain = QLabel(order[i][3])
            chest_pain.setAlignment(QtCore.Qt.AlignCenter)
            diabetes = QLabel(order[i][4])
            diabetes.setAlignment(QtCore.Qt.AlignCenter)
            hta = QLabel(order[i][5])
            hta.setAlignment(QtCore.Qt.AlignCenter)
            dysli = QLabel(order[i][6])
            dysli.setAlignment(QtCore.Qt.AlignCenter)
            smoke = QLabel(order[i][7])
            smoke.setAlignment(QtCore.Qt.AlignCenter)
            cacs = QLabel(order[i][8])
            cacs.setAlignment(QtCore.Qt.AlignCenter)
            model = QLabel(order[i][9])
            model.setAlignment(QtCore.Qt.AlignCenter)
            risk = QLabel(str(order[i][10]))
            risk.setAlignment(QtCore.Qt.AlignCenter)
            
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
ORDERED WORK LIST OF EACH PHYSICIAN (version 3)
"""
class WorkingList (QMainWindow):
#class LogIn(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi('gui_worklist3.ui',self)
        self.setWindowTitle('Working List')
        
        # Access the grid layout from the loaded UI
        self.grid_layout = self.gridLayout
        
        self.parent = parent
        self.main_class = self.parent.parent.main_class
        order = self.main_class.get_order4validation()
        #print('FIRST ORDER: ',order)
        num_patients = len(order)
        #print('ORDER AFTER MAIN: ',order)
         
        for i in range(num_patients):
            #Add rows with labels and buttons based on the specified number input
            ident = order[i][0]
            info = QPushButton("+")
            num_order = QLabel(f"{i+1}")
            num_order.setAlignment(QtCore.Qt.AlignCenter)
            name = QLabel(order[i][1])
            name.setAlignment(QtCore.Qt.AlignCenter)
            urgency = QLabel(order[i][2])
            urgency.setAlignment(QtCore.Qt.AlignCenter)
            cadrads = QLabel(order[i][3])
            cadrads.setAlignment(QtCore.Qt.AlignCenter)
            motive = QLabel(order[i][7])
            urg_std = QLabel(str(order[i][8]))
            urg_std.setAlignment(QtCore.Qt.AlignCenter)
            
            #label of buttons call2action depending whether the patient has/has not preliminary report
            if order[i][3] != "-":
                action = QPushButton("Validate")
            else:
                action = QPushButton("Report")
            
            #coloring of priority groups
            if order[i][2] == "Urgent":
                urgency.setStyleSheet("color: red; font-weight: bold")
                urgency.setText('High priority')
                cadrads.setText(order[i][3]+'*')
                cadrads.setStyleSheet('font-weight: bold')
            elif order[i][2] == "High priority":
                urgency.setStyleSheet("color: orange; font-weight: bold")
                urgency.setText('Medium priority')
            else:
                urgency.setStyleSheet("color: green; font-weight: bold")
            
            #mark in bold the cases that are first because they are marked as urgent
            if order[i][8] == True:
                urg_std.setStyleSheet("background-color: red; color: white; font-weight: bold")
            
            action.clicked.connect(lambda _, ident=ident: self.on_button_clicked(ident))
            info.clicked.connect(lambda _, ident=ident: self.explainability_more_info(ident))
                        
            self.grid_layout.addWidget(urg_std,i+2,2)
            self.grid_layout.addWidget(num_order,i+2,3)
            self.grid_layout.addWidget(name,i+2,4)
            self.grid_layout.addWidget(urgency,i+2,5)
            self.grid_layout.addWidget(cadrads,i+2,6)
            self.grid_layout.addWidget(motive,i+2,7)
            self.grid_layout.addWidget(info,i+2,8)
            self.grid_layout.addWidget(action,i+2,9)
            
                        
    def on_button_clicked(self, identifier):
        #identifier = label.text()
        #self.main_class.set_reportGeneration(self.main_class.get_imgAnalysis(),identifier)
        global report_coronaries
        report_coronaries = ReportCoronaries(identifier,self.main_class)
        report_coronaries.setGeometry(0,0,1250,900)
        report_coronaries.show()
        
    def explainability_more_info(self,identifier):
        #identifier = label.text()
        
        if identifier in self.main_class.get_imgAnalysis().keys():
            global more_info
            more_info = Exp_order_AI(self,identifier)
            more_info.show()
        elif identifier in self.main_class.get_filtering()[1].keys():
            global more_info2
            more_info2 = Exp_order_nonAI(self,identifier)
            more_info2.show()

"""
EXPLAINABILITY OF WORKING LIST ORDER
"""
# Explainability for patients going through AI-workflow
class Exp_order_AI (QMainWindow):
#class LogIn(QWidget):
    def __init__(self,parent,identifier):
        super().__init__(parent)
        uic.loadUi('gui_PriorityExp_AI.ui',self)
        self.setWindowTitle('Explainability')
        self.setGeometry(10,100,650,750)
        
        self.ident = identifier
        self.main_class = parent.main_class
        
        consult_motive = self.main_class.get_imgAnalysis()[self.ident]['EHR']['Consult motive']
        try:
            chest_pain = self.main_class.get_imgAnalysis()[self.ident]['EHR']['Chest pain']
        except:
            chest_pain = 'No'
        previous_proc = self.main_class.get_imgAnalysis()[self.ident]['EHR']['Previous procedures']
        previous_proc_list = [x for x in previous_proc if x is not False]
        pre_test_score = self.main_class.get_imgAnalysis()[self.ident]['Pre-test score']
        urgency = self.main_class.get_imgAnalysis()[self.ident]['EHR']['Urgent study']
        
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
        
        LAD = max(LAD_stenosis)
        Cx = max(Cx_stenosis)
        RCA = max(RCA_stenosis)
        
        self.clinical_info_text.setText(f'- Patient presenting {chest_pain} chest pain and under the consultation motive: {consult_motive}.\n- Patient has a Pre-Test Risk Score of {pre_test_score}%.')
        if previous_proc_list == []:
            self.clinical_info_text.append('- Patient does not have any previous procedures reported.')
        else:
            previous_proc_text = []
            self.append_string_with_space(self,previous_proc_text,'- Patient has the following previous procedures reported:')
            for i in previous_proc_list:
                self.append_string_with_space(self,previous_proc_text,str(i))
            self.clinical_info_text.append("".join(previous_proc_text))
        if urgency == False:
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
        self.image_info_text.append(f'Maximum stenosis degrees of the main vessels are LAD={LAD}, Cx={Cx} and RCA={RCA}.')
        self.image_info_text.append(f'\nPatient presents a detected calcium score of {CACS} through Agatston score.')
        
        self.clinical_info_text.setEnabled(False)
        self.image_info_text.setEnabled(False)
        
        pixmapLAD = QPixmap(self.CPR_vessel('LAD'))
        self.LAD_CPR.setPixmap(pixmapLAD)
        pixmapCx = QPixmap(self.CPR_vessel('Cx'))
        self.Cx_CPR.setPixmap(pixmapCx)
        pixmapRCA = QPixmap(self.CPR_vessel('RCA'))
        self.RCA_CPR.setPixmap(pixmapRCA)
               
    def CPR_vessel(self,vessel):
        vessel = 'CPR'+'_'+vessel
        directory = os.getcwd()
        cpr_path = os.path.join(directory, 'Case1_ASOCA','CPR',vessel)
        cpr_image = cpr_path+'.png'
        return cpr_image
        
    def append_string_with_space(self,list_of_strings,string):
        list_of_strings.append(string)
        list_of_strings.append(" ")

# Explainability for patients not going through AI-workflow

class Exp_order_nonAI (QMainWindow):
#class LogIn(QWidget):
    def __init__(self,parent,identifier):
        super().__init__(parent)
        uic.loadUi('gui_PriorityExp_nonAI.ui',self)
        self.setWindowTitle('Explainability')
        self.setGeometry(10,100,650,350)
        
        self.ident = identifier
        self.main_class = parent.main_class
        
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
        
    def append_string_with_space(self,list_of_strings,string):
        list_of_strings.append(string)
        list_of_strings.append(" ")


"""
CCTA VIEWER CODE v02
"""
def read_img_nii(img_path):
    image_data = np.array(nib.load(img_path).get_fdata())
    return image_data

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

class MatplotlibCanvas(FigureCanvas):
    def __init__(self, img_path, img_path_2):
        self.fig, self.axes = plt.subplots(2, 2)  # Create a 2x2 grid of subplots
        self.img_data = read_img_nii(img_path)
        self.img_data_2 = read_img_nii(img_path_2)
        self.current_layer = [0, 0, 0]  # Initialize current layer for each view
        self.views = ['axial', 'coronal', 'sagittal']
        self.overlay = True  # Initialize with overlay on

        super().__init__(self.fig)

        self.plot()

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

    def update_plot(self):
        self.fig.clf()  # Clear the figure
        self.axes = self.fig.subplots(2, 2)  # Redefine subplots
        self.plot()

class ImageViewerWidget(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.layout = QVBoxLayout()

        self.slider = QSlider()
        self.slider.setMinimum(0)
        self.slider.setMaximum(511)  # Set maximum value for coronal and sagittal views
        self.slider.valueChanged.connect(self.slider_changed)

        self.layout.addWidget(self.slider)

        self.combo = QComboBox()
        self.combo.addItem("Overlayed segmentation")
        self.combo.addItem("Raw CCTA")
        self.combo.currentIndexChanged.connect(self.combo_changed)

        self.layout.addWidget(self.combo)
        self.setLayout(self.layout)

    def slider_changed(self, value):
        for i in range(3):
            if self.parent.canvas.views[i] == 'axial':
                self.parent.canvas.current_layer[i] = min(value, 203)  # Limit the axial view slider to 203
            else:
                self.parent.canvas.current_layer[i] = value
        self.parent.canvas.update_plot()

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
REPORTING AND VALIDATION
"""
class ReportCoronaries(QMainWindow):
    def __init__(self,identifier,main_class):
        super().__init__()
        #self.window_state = self.saveState()
        uic.loadUi('gui_report_coronaries2.ui',self)
        self.setWindowTitle('Reporting System')
        
        self.ident = identifier
        self.main_class = main_class 
        if self.ident in self.main_class.get_imgAnalysis().keys():
             self.main_class.get_imgAnalysis()['validated_identifiers'] = []
        #self.report_window = ReportCoronaries(self.ident,self.main_class)
        
        self.report_general = [self.FemaleSex,self.MaleSex,self.textAge,self.UrgentStudy,self.textPhysician,self.textHospital,self.textService,self.dateStudy,self.optionDominance,self.optionCACs]
        self.database_general = ['Sex','Age','Urgent study','Physician','Center','Service','Study date','Dominance','CACs']
        #self.report_segments = [self.optionLCA,self.optionpLAD,self.optionmLAD,self.optiondLAD,self.optionD1,self.optionD2,self.optionpCx,self.optionmCx,self.optiondCx,self.optionOM1,self.optionOM2,self.optionLPD,self.optionLPL,self.optionRI,self.optionpRCA,self.optionmRCA,self.optiondRCA,self.optionRPD,self.optionRPL]
        self.report_segments = [self.optionLCA,self.optionpLAD,self.optionmLAD,self.optiondLAD,self.optionD1,self.optionD2,self.optionpCx,self.optiondCx,self.optionOM1,self.optionOM2,self.optionLPD,self.optionLPL,self.optionRI,self.optionpRCA,self.optionmRCA,self.optiondRCA,self.optionRPD,self.optionRPL]
        #self.database_segments = ['LCA','p-LAD','m-LAD','d-LAD','D1','D2','p-Cx','m-Cx','d-Cx','OM1','OM2','LPD','LPL','RI','p-RCA','m-RCA','d-RCA','RPD','RPL']
        self.database_segments = ['LCA','p-LAD','m-LAD','d-LAD','D1','D2','p-Cx','d-Cx','OM1','OM2','LPD','LPL','RI','p-RCA','m-RCA','d-RCA','RPD','RPL']
        self.dominance_options = ['Right dominance','Left dominance','Codominance']
        self.CACs_options = [range(0,1),range(1,11),range(11,101),range(101,401),range(401,10000)]
        self.stenosis_options = ['0','1-24','25-49','50-69','70-99','100']
        self.CADRADS_options = ['0','1','2','3','4A','4B','5']
        
        self.AI_info_label.setStyleSheet("color: red;")
        ai_indicator = [self.as1,self.as2,self.as3,self.as4,self.as5,self.as6,self.as7,self.as8,self.as9,self.as10,self.as11,self.as12,self.as13,self.as14,self.as15,self.as16,self.as17,self.as18,self.as19,self.as20]
        for indicator in ai_indicator:
            indicator.setStyleSheet("color: red;")
        
        # Set the initial selection of the combo box based on the random variable
        self.set_combobox_selection()
        
        for i in self.report_segments:
            i.currentIndexChanged.connect(self.changed_stenosis)
            i.currentIndexChanged.connect(lambda _, i=i: self.changed_index(i))
        
        self.optionDominance.currentIndexChanged.connect(lambda _, i=i: self.changed_index(self.optionDominance))
        self.previous_dominance = self.optionDominance.currentIndex()
        self.optionDominance.currentIndexChanged.connect(self.changed_dominance)
        
        self.optionCACs.currentIndexChanged.connect(lambda _, i=i: self.changed_index(self.optionCACs)) 
        
        self.ValidateReport.clicked.connect(self.validate_report)
        self.VisualSupport.clicked.connect(self.visual_support)
        
    def set_combobox_selection(self):
        if self.ident in self.main_class.get_imgAnalysis().keys():
            self.textID.setText(self.ident)
            #self.textID.setReadOnly(True)
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
                    #self.report_general[i+1].setReadOnly(True)
                    self.report_general[i+1].setEnabled(False)
                elif i == 2:
                    if self.main_class.get_imgAnalysis()[self.ident]['EHR'][self.database_general[i]] == 'Yes':
                        self.report_general[i+1].setChecked(True)
                    self.report_general[i+1].setEnabled(False)
                elif i==3 or i==4 or i==5:
                    self.report_general[i+1].setText(str(self.main_class.get_imgAnalysis()[self.ident]['Admin'][self.database_general[i]]))
                    #self.report_general[i+1].setReadOnly(True)
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
                    #self.report_general[i+1].setStyleSheet("background-color: purple; color: white;")
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
    
    def changed_stenosis(self):
        modified_stenosis = []
        for i in self.report_segments:
            modified_stenosis.append(i.currentText())
        if '100%' in modified_stenosis: 
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
    
    def assign_color(self,combobox):
        if combobox.currentIndex() == 0:
            combobox.setStyleSheet("background-color: grey; color: black;")
        elif combobox.currentIndex() == 1:
            combobox.setStyleSheet("background-color: green; color: black;")
        elif combobox.currentIndex() == 2:
            combobox.setStyleSheet("background-color: yellow; color: black;")
        elif combobox.currentIndex() == 3:
           combobox.setStyleSheet("background-color: orange; color: black;")
        elif combobox.currentIndex() == 4:
            combobox.setStyleSheet("background-color: pink; color: black;")
        elif combobox.currentIndex() == 5:
            combobox.setStyleSheet("background-color: red; color: white;")
        elif combobox.currentIndex() == 6:
            combobox.setStyleSheet("background-color: black; color: white;")
        elif combobox.currentIndex() == 7:
            combobox.setStyleSheet("background-color: purple; color: white;")
        
    
    def changed_index(self,combobox):
        segments = [self.as3,self.as4,self.as5,self.as6,self.as7,self.as8,self.as9,self.as10,self.as11,self.as12,self.as13,self.as14,self.as15,self.as16,self.as17,self.as18,self.as19,self.as20]
        if combobox == self.optionDominance: 
            self.as1.setText('')
        elif combobox == self.optionCACs:
            self.as2.setText('')
        else:
            segments[self.report_segments.index(combobox)].setText('')
            self.assign_color(combobox)
    
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
    
    def validate_report(self):
        # Close the current window
        self.close()
        """
        if self.ident in self.main_class.get_imgAnalysis().keys():
            self.main_class.get_imgAnalysis()['validated_identifiers'].append(self.ident)
            print(self.main_class.get_imgAnalysis()['validated_identifiers'])
            self.close()
            WorkingList(self.main_class).update_window()
            global working_list
            working_list = WorkingList(self.main_class)
            working_list.inactivate_validated_case(self.main_class.get_imgAnalysis()['validated_identifiers'])
            working_list.show()
        """
        # Generate a new window
        global final_report
        #final_report = FinalReport(self.ident,self.main_class,self.textID,self.FemaleSex,self.MaleSex,self.textAge,self.UrgentStudy,self.textPhysician,self.textHospital,self.textService,self.dateStudy,self.optionDominance,self.optionCACs,self.optionLCA,self.optionpLAD,self.optionmLAD,self.optiondLAD,self.optionD1,self.optionD2,self.optionpCx,self.optiondCx,self.optionOM1,self.optionOM2,self.optionLPD,self.optionLPL,self.optionRI,self.optionpRCA,self.optionmRCA,self.optiondRCA,self.optionRPD,self.optionRPL,self.optionCADRADS,self.optionPlaque,self.optionN,self.optionHRP,self.optionIschemia,self.optionS,self.optionG,self.optionE,self.textEdit)
        final_report = FinalReport(self)
        final_report.setGeometry(0,0,1250,900)
        final_report.show()
    
    def visual_support(self):
        run_viewer()
        
        directory = os.getcwd()
        stl_path = os.path.join(directory, 'Case1_ASOCA','Normal_1.stl')
        
        global cpr_view
        cpr_view = CPR_Viewer(self)
        cpr_view.setGeometry(600,700,1200,300)
        cpr_view.show()
        
        mesh = o3d.io.read_triangle_mesh(stl_path)
        mesh = mesh.compute_vertex_normals()
        o3d.visualization.draw_geometries([mesh], window_name="Segementation View", left=550, top=80, width=500, height=500)

"""
CPR viewer window
"""
class CPR_Viewer(QMainWindow):
    def __init__(self,parent):
        super().__init__(parent)
        uic.loadUi('gui_CPRviewer.ui',self)
        self.setWindowTitle("Curved Planar Reformation (CPR) Viewer")
        self.selector.currentIndexChanged.connect(self.changed_vessel)
        self.parent = parent
        
    def changed_vessel(self):
        vessel = 'CPR'+'_'+self.selector.currentText()
        #print('Selected vessel for CPR: ',vessel)
        directory = os.getcwd()
        cpr_path = os.path.join(directory, 'Case1_ASOCA','CPR',vessel)
        cpr_image = cpr_path+'.png'
        pixmap = QPixmap(cpr_image)
        self.CPR.setPixmap(pixmap)
        
"""
FINAL REPORT VISUALIZATION
"""
class FinalReport(QMainWindow):
    #def __init__(self,ident,main_class,textID,FemaleSex,MaleSex,textAge,UrgentStudy,textPhysician,textHospital,textService,dateStudy,optionDominance,optionCACs,optionLCA,optionpLAD,optionmLAD,optiondLAD,optionD1,optionD2,optionpCx,optiondCx,optionOM1,optionOM2,optionLPD,optionLPL,optionRI,optionpRCA,optionmRCA,optiondRCA,optionRPD,optionRPL,optionCADRADS,optionPlaque,optionN,optionHRP,optionIschemia,optionS,optionG,optionE,textEdit):
    def __init__(self,parent):
        super().__init__()
        uic.loadUi('gui_FINALreport_coronaries2.ui',self)
        self.setWindowTitle('Final Report')
        self.parent = parent
        self.ident = self.parent.ident
        self.main_class = self.parent.main_class
        
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
        self.optionLCA.setCurrentIndex(self.parent.optionLCA.currentIndex())
        self.optionLCA.setEnabled(False)
        self.optionpLAD.setCurrentIndex(self.parent.optionpLAD.currentIndex())
        self.optionpLAD.setEnabled(False)
        self.optionmLAD.setCurrentIndex(self.parent.optionmLAD.currentIndex())
        self.optionmLAD.setEnabled(False)
        self.optiondLAD.setCurrentIndex(self.parent.optiondLAD.currentIndex())
        self.optiondLAD.setEnabled(False)
        self.optionD1.setCurrentIndex(self.parent.optionD1.currentIndex())
        self.optionD1.setEnabled(False)
        self.optionD2.setCurrentIndex(self.parent.optionD2.currentIndex())
        self.optionD2.setEnabled(False)
        self.optionpCx.setCurrentIndex(self.parent.optionpCx.currentIndex())
        self.optionpCx.setEnabled(False)
        self.optiondCx.setCurrentIndex(self.parent.optiondCx.currentIndex())
        self.optiondCx.setEnabled(False)
        self.optionOM1.setCurrentIndex(self.parent.optionOM1.currentIndex())
        self.optionOM1.setEnabled(False)
        self.optionOM2.setCurrentIndex(self.parent.optionOM2.currentIndex())
        self.optionOM2.setEnabled(False)
        self.optionLPD.setCurrentIndex(self.parent.optionLPD.currentIndex())
        self.optionLPD.setEnabled(False)
        self.optionLPL.setCurrentIndex(self.parent.optionLPL.currentIndex())
        self.optionLPL.setEnabled(False)
        self.optionRI.setCurrentIndex(self.parent.optionRI.currentIndex())
        self.optionRI.setEnabled(False)
        self.optionpRCA.setCurrentIndex(self.parent.optionpRCA.currentIndex())
        self.optionpRCA.setEnabled(False)
        self.optionmRCA.setCurrentIndex(self.parent.optionmRCA.currentIndex())
        self.optionmRCA.setEnabled(False)
        self.optiondRCA.setCurrentIndex(self.parent.optiondRCA.currentIndex())
        self.optiondRCA.setEnabled(False)
        self.optionRPD.setCurrentIndex(self.parent.optionRPD.currentIndex())
        self.optionRPD.setEnabled(False)
        self.optionRPL.setCurrentIndex(self.parent.optionRPL.currentIndex())
        self.optionRPL.setEnabled(False)
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
        
        self.reported_vessels = [self.optionLCA,self.optionpLAD,self.optionmLAD,self.optiondLAD,self.optionpCx,self.optiondCx,self.optionD1,self.optionD2,self.optionOM1,self.optionOM2,self.optionLPD,self.optionLPL,self.optionRI,self.optionpRCA,self.optionmRCA,self.optiondRCA,self.optionRPD,self.optionRPL]
        self.name_vessels = ['LCA','p-LAD','m-LAD','d-LAD','p-Cx','d-Cx','D1','D2','OM1','OM2','LPD','LPL','RI','p-RCA','m-RCA','d-RCA','RPD','RPL']
        
        for vessel in self.reported_vessels:
            self.parent.assign_color(vessel)
        
        self.reported_degree = ['0%','<25%','<50%','<70%','<99%','100%','NEv']
        self.degree = ['0','1-24','25-49','50-69','70-99','100','NA']
        self.calcium = ['','0','1-10','11-100','101-400','>400','NA']
        
        self.update_records()
        self.pushButton_3.clicked.connect(self.report_button)
    
    def update_records(self):
        if self.ident in self.main_class.get_imgAnalysis().keys():
            for i in range(len(self.reported_vessels)):
                for j in self.main_class.get_imgAnalysis()[self.ident]['Stenosis']:
                    if self.main_class.get_imgAnalysis()[self.ident]['Stenosis'][j][1] == self.name_vessels[i]:
                        index = self.reported_degree.index(self.reported_vessels[i].currentText())
                        self.main_class.get_imgAnalysis()[self.ident]['Stenosis'][j][0] = self.degree[index]
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
            self.main_class.get_imgAnalysis()[self.ident]['Graph']=True if self.optionG.isChecked() else False
            self.main_class.get_imgAnalysis()[self.ident]['Exceptions']=True if self.optionE.isChecked() else False
            self.main_class.get_imgAnalysis()[self.ident]['Ischemia']=self.optionIschemia.currentText()
            self.main_class.get_imgAnalysis()[self.ident]['Additional comments']=self.textEdit.toPlainText()
        
    def report_button(self):
        self.main_class.set_reportGeneration(self.main_class.get_imgAnalysis(),self.ident,1)
        report = self.main_class.get_reportGeneration()
        global reportRIS
        reportRIS = report_RIS(report)
        reportRIS.show()
        
"""
WRITTEN REPORT FOR RIS UPLOAD
"""
class report_RIS(QMainWindow):
    def __init__(self,report):
        super().__init__()
        uic.loadUi('gui_report_RIS.ui',self)
        self.setWindowTitle('RIS report')
        self.report = report
        self.strings = []
        for string in self.report:
            self.append_string_with_newline(string)
                
        # Join the strings with space and set them to the text edit
        self.Report.setPlainText("".join(self.strings))    
        #self.Report.setPlainText("\n".join(self.strings))
        self.save.clicked.connect(self.save_text)
        
    def append_string_with_newline(self,string):
        # Append string to the list with a new line
        self.strings.append(string)
        self.strings.append("\n")
    
    def append_string_with_space(self,string):
        self.strings.append(string)
        self.strings.append(" ")
            
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
                
            
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = LogIn()
    GUI.show()
    sys.exit(app.exec_())