# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 21:36:50 2024

@author: ferbe
"""
import random

class ImageAcquisition:
    def __init__(self):
        self.image_quality = ['Good','Adequate','Deficient']
        self.limitations = ['Cardiac motion artifact',
                            'Respiratory motion artifact',
                            'Reconstructive artifact',
                            'Venous interposition',
                            'Poor opacification',
                            'Granular image (low S/R)',
                            'Excessive coronary calcification',
                            'Metallic artifacts'
                            ]
    def take_ccta(self,database,order):
        # Patient generation of information from the image in order of priority
        for i in order:
            quality = random.choices([self.image_quality[0],self.image_quality[1],self.image_quality[2]],weights=(0.88,0.08,0.04))[0] # real data percentages
            limits = []
            for j in range(8):
                choice = random.choices([self.limitations[j],False],weights=(0.005,0.995))
                limits.extend(choice)
            database[i[0]]['Quality'] = quality
            database[i[0]]['Limitations'] = limits
        return database