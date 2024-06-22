from tabulate import tabulate

class Filtering:
    # filtering patients for automatic image analysis considering only factors from before the image acquisition
    def filtering_preimage(self,database):
        for i in database: 
            if (any(database[i]['EHR']['Previous procedures'])):              
                database[i]['first_filter'] = False
            else: 
                database[i]['first_filter'] = True
        return database
    
    # filtering patients for automatic image analysis considering only factors from after the image acquisition
    def filtering_postimage(self,database):
        for i in database: 
            if database[i]['first_filter']: # only if the filter from before the image acquisition has been passed
                if (any(database[i]['Limitations']) or database[i]['Quality']=='Deficient'):
                    database[i]['second_filter'] = False
                else: 
                    database[i]['second_filter'] = True
        return database

    # separation of patients into two databases between non-suitable and suitable to undergo the automatic AI image analysis
    def filtering(self,database):
        reporting_list = []
        database_preimage = self.filtering_preimage(database) # filter before image acquisition
        database_postimage = self.filtering_postimage(database_preimage) # re-filter after image acquisition
        
        database_AI = {} # database of patients undergoing automatic AI image analysis
        database_notAI = {} # database of patients not undergoing automatic AI image analysis
        
        for i in database_postimage: 
            if database_postimage[i]['first_filter']:
                if database_postimage[i]['second_filter']:
                    reporting_list.append([i,'Yes','Yes','Suitable'])
                    database_postimage[i]['AI suitability'] = True
                    database_AI[i] = database_postimage[i] # patient undergoing automatic AI image analysis
                else:
                    reporting_list.append([i,'Yes','No','-'])
                    database_postimage[i]['AI suitability'] = False
                    database_notAI[i] = database_postimage[i] # patient not undergoing automatic AI image analysis
            else: 
                reporting_list.append([i,'No','-','-'])
                database_postimage[i]['AI suitability'] = False
                database_notAI[i] = database_postimage[i] # patient not undergoing automatic AI image analysis
        
        return database_AI, database_notAI
    
    # algorithm that explains why a specific patient is suitable or not suitable for automatic AI image analysis by explianing:
        # - whether the patient has any previous procedures
        # - whether the image quality is deficient
        # - whether the image study has suffered some limitations during the acquisition
    def explainability_suitability(self,data,identifier):
        print('\n\033[1m'+f'SUITABILITY FOR AI WORKFLOW OF PATIENT {identifier}'+'\033[0m\n')

        pre_proc = []
        for i in data[identifier]['EHR']['Previous procedures']: 
            if i:
                pre_proc.append(i)
        lim = []
        for i in data[identifier]['Limitations']:
            if i:
                lim.append(i)

        reporting = [identifier,
                     data[identifier]['AI suitability'],
                     pre_proc if pre_proc!=[] else '-',
                     data[identifier]['Quality'],
                     lim if lim!=[] else '-']
        print(tabulate([reporting],headers=['Patient ID','Suitability','Prev. procedures','Quality','Limitations']))