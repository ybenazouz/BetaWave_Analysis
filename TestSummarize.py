"""
Python script to anonymize and store data from JSon files of patients with DBS. 
Data extracted from the json files by means of the Summarize2.py app will be put accordingly into the main excel sheet.
The data will also be anonymized, using a anonymization key. 

Author: 
Yasmin Ben Azouz
TM2 Intership 3
Neurosurgery Department
Haga Hospital, The Hague 

Modules to download before using the code: 
- pip install openpyxl
"""
# Imports 
import json  # Import json module to process json files
import os  # Import os module to create directories
import pathlib  # import Pathlib module to create directories
from datetime import date, datetime
#import loading_path as lp
from pathlib import Path
from tkinter import \
    Tk  # Import tkinter module to create window in which a file can be selected
from tkinter.filedialog import \
    askdirectory  # Show window to select json file to be analyzed
from tkinter.filedialog import \
    askopenfilename  # Show window to select json file to be analyzed
import pandas as pd
import math as math 

# Import selfmade functions 
from open_json import open_json

import numpy as np

# from loading_data import loading_data

# Step 1: retrieve folder with all summarise3 information 
Tk().withdraw()                         # we don't want a full GUI, so keep the root window from appearing
dir_sum = askdirectory()      # show an "Open" dialog box and return the path to the selected directory 
                                    # This should be the Summarise3 folder
# Old Data 
od = pd.read_excel(pathlib.PurePath(dir_sum, 'output.xlsx'))    # read the .xlsx file as a panda datastruct 
od['MeasureDate'] = pd.to_datetime(od['MeasureDate']).dt.date   # remove time from measuredate 

old_name = 'Summarize3_archived_' +str(datetime.now().strftime("%Y-%m-%d %H.%M") )+ '.xlsx'  # Generate new name for old file that will be archived
archive = pathlib.PurePath(dir_sum, 'Archive')  # generate Path to archive 
od.to_excel(pathlib.PurePath(archive, old_name)) # Generate new .xlsx file for archive and add to archive folder

# Anonymization Key 
anon = pd.read_excel(pathlib.PurePath(dir_sum, 'Anonymisation.xlsx'))    # read the .xlsx file as a panda datastruct 

# Step 2: retrieve folder with .json files and loop within folder to retrieve information and put in struct
Tk().withdraw()                 # we don't want a full GUI, so keep the root window from appearing
directory_json = askdirectory() # show an "Open" dialog box and return the path to the selected directory 
                                # The directory should be a folder with JSON files you want to check and add to the xlsx.
                                                               
new_data = []                   # Create list to append lists with data to
for filename in os.listdir(directory_json):
    if filename !='.DS_Store':  # Hidden files in macbooks. 
    # open_json function >> is het handiger de if loop hiervoor te beginnen? Zit er nu in? Of vanaf data? 
        for first in s: 
            list = open_json(directory_json, filename, anon)
            new_data.append(list)       # Append new row of data for each list. 
            print(first)

nd = pd.DataFrame(new_data)     # Turn list with all data to datastruct
nd.columns = ['Patient','MeasureDate', 'StimulatorType', 
        'P6channel', 'P6rec', 'P6time',
        'P7channel', 'P7rec', 'P7time',
        'P11channel', 'P11rec', 'P11time', 'P11time2',
        'P2channel', 'P2rec', 'P2time',
        'P1DateTime', 
        'P3DateEnd', 'P3DateStart', 'P3Days', 'P3end', 'P3start', 
        'P9Events', 
        'P4firstname', 'P4lastname', 'P4patientID']

# Step 5: check data (doubles, arrange) 

# Doubles 
ad = pd.concat([od, nd], ignore_index=True) # Concatenate old data and new data to check for doubles
ad2 = ad.iloc[ad.astype(str).drop_duplicates().index] # Drop doubles >> Return bool series to see which ones are double? 

arrays = np.array(ad2['Patient'], ad2['Measuredate'])

# Arrange 



# ------------------------------------------------------------------------------------------------------
# TRASH 

#------14.11.22---------

##dd = ad.drop(['P6channel', 'P7channel', 'P11channel', 'P2channel'], axis=1)
##ad = ad.drop([1, 2])
##print(ad)

##bs = ad['StimulatorType'].astype(str).duplicated()
##bs2 = ad['P6channel'].astype(str).duplicated()
##bs3 = ad['P6rec'].astype(str).duplicated()
##bs4 = ad['P6time'].astype(str).duplicated()
##bs5 = ad['P7channel'].astype(str).duplicated()
##bs8 = ad['P7rec'].astype(str).duplicated()
##bs9 = ad['P7time'].astype(str).duplicated()
##bs10 = ad['P11channel'].astype(str).duplicated()
##bs11 = ad['P11rec'].astype(str).duplicated()
##bs12 = ad['P11time'].astype(str).duplicated()
##bs13 = ad['P11time2'].astype(str).duplicated()
##bs14 = ad['P2channel'].astype(str).duplicated()
##bs15 = ad['P2rec'].astype(str).duplicated()
##bs16 = ad['P2time'].astype(str).duplicated()
##bs17 = ad['P1DateTime'].astype(str).duplicated()
##bs18 = ad['P3DateEnd'].astype(str).duplicated()
##bs19 = ad['P3DateStart'].astype(str).duplicated()
##bs20 = ad['P3Days'].astype(str).duplicated()
##bs21 = ad['P3end'].astype(str).duplicated()
##bs22 = ad['P3start'].astype(str).duplicated()
##bs23 = ad['P9Events'].astype(str).duplicated()
##print(bs,bs2,bs3,bs4,bs5,bs8,bs9,bs10,bs11,bs12,bs13,bs14,bs15,bs16,bs17,bs18,bs19,bs20,bs21,bs22, bs23)
        #'P4firstname', 'P4lastname', 'P4patientID'].astype(str).duplicated() #drop_duplicates().index]
# bool_series = ad.duplicated() #(keep='first')   # Remove duplicates
## pd.set_option('display.max_columns', None)
## ad.head()

#---- 15.11.22 --------------

#directory_anon = askopenfilename() 

## pat_id = anon.loc[:,"Patient ID"]       # retrieve the patient id's from the data stuct 
## pat_name = anon.loc[:,"Patient Name"]   # retieve the patient names from the data struct 
## pat = anon.loc[:,"Patient Number"]      # retrieve replacement patient number

#---- 16.11.22 ------------------

#bs = row['FirstName'].equals(pid['FirstName'])
#bs2 = row['LastName'].equals(pid['LastName'])

## apid = pd.concat([anon, pid], ignore_index=True)
##bs = apid[apid['FirstName'].duplicated(keep=False)]
##bs2 = apid[apid['LastName'].duplicated(keep=False)]
##bs3 = apid[apid['ID'].duplicated(keep=False)]
#print(bs3)

##bs = bs.groupby(list[bs]).apply(lambda x: tuple(x.index)).tolist()
##bs2 = bs2.groupby(list[bs2]).apply(lambda x: tuple(x.index)).tolist()
##bs3 = bs3.groupby(list[bs3]).apply(lambda x: tuple(x.index)).tolist()

# Anonymize ------------------------
## anon_id = []  # create struct for id to fit in 
## for index2, row2 in pid.iterrows():  # loop through new patient information # DOUBLES NIET VERWIJDERD IN DEZE DATA 
    ## anon_row = [] # create studt 
    ## for index, row in anon.iterrows():  # Loop through key information 
        ## if not math.isnan(row['ID']):
            # ook if anon is float vlaue voor omzetten integer? maakt dat uit? 
            ## id = math.floor(row['ID']) # turn float patient id into integer using numpy series   
            ## if id == row2['ID']: 
                ## anon_row = row['Pseudo']
        ## elif row['LastName'] == row2['LastName']:
            ## anon_row = row['Pseudo']   
    ## if anon_row != []: 
        ## anon_id.append(anon_row)
    ## else: 
        ## anon_id.append('Unknown')   
        # controle of anon_id even lang is als het aantal rijen in pid? 
        # Controleren of er unknown identity staat etc? 
        # Controleren of het een onbekende patient naam en id is? In dit geval melding geven om toe te voegen in de key?      
#print(anon_id)

## pid = nd[['P4firstname', 'P4lastname', 'P4patientID']] # create patient id with name and id to compare to key

# Test patient id 
## data = [['Ben', 'Azouz', float('nan')], [float('nan'), 'Draad',44444], [float('nan'), 'Azouz', 33445]]
## pid = pd.DataFrame(data, columns=['FirstName', 'LastName', 'ID'])

#------21.11.2022 ---------------
#print(anon['Pseudo'].tolist(), 
            #ad2['MeasureDate'].tolist())
#arrays = [anon['Pseudo'], 
            #ad2['MeasureDate']]
#tuples = list(zip(*arrays))
#ind = pd.MultiIndex.from_tuples(tuples, names=["Pseudo", "MeasureDate"])

#for apid in anon['Pseudo']


#ad3 = ad2.drop(['P4firstname', 'P4lastname', 'P4patientID'], axis=1)    # remove personal information (moet dit?)
#ad3.insert(0,'Pseudo', anon_id)     # add pseudo number to the front of dataframe

#ad3.set_index('Pseudo') # set 'Pseudo' as new index instead of usual indexing 
#print(ad3)

# is het niet handiger om de bestaande structuur te behouden en alleen nieuwe rijen toe te voegen
#order = anon['Pseudo']
#ad4 = ad3.reindex(anon['Pseudo'])
#print(ad4)

#final = pd.DataFrame(index={'Pseudo':anon['Pseudo']})

# Stappenplan
# 1. xlsx downloaden met alle data 
# 2. xlsxl met sleutelbestand 
# 3. json bestanden selecteren en tellen hoe veel het er zijn
# 4. loop starten, data er uit halen 
# 5. check de data met de data die er al in staat, als niet dubbel voeg dan data toe 
# 6. report maken van wat wel en niet is toegevoegd???
# 7. anonymized json file uitgeven ook?? 