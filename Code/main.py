# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 21:53:27 2024

@author: ferbe
"""
from Initial_Patient_Generation import Initial_Patient_Generation
from PreTestScore import PreTestScore
from ImageAcquisition import ImageAcquisition
from Filtering import Filtering
from ImageInfo_Generator import ImageInfo_Generator
from Report_Generation import Report_Generation
from Prioritization_Validation import Prioritization_Validation

class main:
    def __init__(self,num_patients=10):
        self.initial_patients = Initial_Patient_Generation(num_patients).generate_initial_pool()
        self.order_img_acquisition = self.order4image(self.initial_patients)
        self.patients_img_info = self.imageAcquisition(self.initial_patients,self.order_img_acquisition)
        self.patients_AI, self.patients_notAI = self.filtering(self.patients_img_info)
        self.analysed_img = self.img_analysis(self.patients_AI)
        self.order_validation = self.order4validation(self.analysed_img,self.patients_notAI)
        #self.report = self.report_generation(self.analysed_img,self.order_validation)
    
    def order4image(self,dic):
        return PreTestScore().order_prioritization(dic)
    
    def imageAcquisition(self,dic,order):
        return ImageAcquisition().take_ccta(dic,order)
        
    def filtering(self,dic):
        return Filtering().filtering(dic)
    
    def explain_filtering(self,dic,identifier):
        return Filtering().explainability_suitability(dic,identifier)
    
    def img_analysis(self,dic):
        analysed_patient_images = ImageInfo_Generator().image_data_generator(dic)
        analysed_patient_images = PreTestScore().assign_risk(analysed_patient_images)
        analysed_patient_images = ImageInfo_Generator().CADRADS_calculator(analysed_patient_images)
        return analysed_patient_images
    
    def order4validation(self,dic_AI,dic_notAI):
        order = Prioritization_Validation(dic_AI,dic_notAI).set_order()
        print("order: ",order)
        return order
    
    def report_generation(self,dic,ident):
        ident = next(iter(dic)) 
        return Report_Generation().show_report(dic,ident,1)   
    
if __name__ == '__main__':
    main()