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
import json                             # Import json module to process json files
import os                               # Import os module to create directories
import pathlib                          # import Pathlib module to create directories
from datetime import date, datetime
#import loading_path as lp
from pathlib import Path
from tkinter import \
    Tk                                  # Import tkinter module to create window in which a file can be selected
from tkinter.filedialog import \
    askdirectory                        # Show window to select json file to be analyzed
from tkinter.filedialog import \
    askopenfilename                     # Show window to select json file to be analyzed
import pandas as pd
import math as math 

# Import selfmade functions 
from open_json import open_json

import numpy as np

# from loading_data import loading_data

# Step 1: retrieve folder with all summarise3 information 
Tk().withdraw()                         # prevent full GUI
dir_sum = askdirectory()                # Show an "Open" dialog box and return the path to the selected directory 
                                        # Summarise3 folder
# Old Data 
od = pd.read_excel(pathlib.PurePath(dir_sum, 'output.xlsx'))    # read the .xlsx file as a panda datastruct 
od['MeasureDate'] = pd.to_datetime(od['MeasureDate']).dt.date   # remove time from measuredate 

old_name = 'Summarize3_archived_' +str(datetime.now().strftime("%Y-%m-%d %H.%M") )+ '.xlsx'  # Generate new name for old file that will be archived
archive = pathlib.PurePath(dir_sum, 'Archive')              # generate Path to archive 
od.to_excel(pathlib.PurePath(archive, old_name))            # Generate new .xlsx file for archive and add to archive folder

# Anonymization Key 
anon = pd.read_excel(pathlib.PurePath(dir_sum, 'Anonymisation.xlsx'))    # read the .xlsx file as a panda datastruct 

# Step 2: retrieve folder with .json files and loop within folder to retrieve information and put in struct
#Tk().withdraw()                                                 # we don't want a full GUI, so keep the root window from appearing
#directory_json = askdirectory()                                 # show an "Open" dialog box and return the path to the selected directory 
                                                                 # The directory should be a folder with JSON files you want to check and add to the xlsx.
                                                               
                                # Hidden files in macbooks. 
    # open_json function >> is het handiger de if loop hiervoor te beginnen? Zit er nu in? Of vanaf data? 
new_data = open_json(dir_sum, anon)
                                # Append new row of data for each list. 

nd = pd.DataFrame(new_data)                                     # Turn list with all data to datastruct
nd.columns = ['Patient','MeasureDate', 'StimulatorType', 
        'P6channel', 'P6rec', 'P6time',
        'P7channel', 'P7rec', 'P7time',
        'P11channel', 'P11rec', 'P11time', 'P11time2',
        'P2channel', 'P2rec', 'P2time',
        'P1DateTime', 
        'P3DateEnd', 'P3DateStart', 'P3Days', 'P3end', 'P3start', 
        'P9Events']
        #'P4firstname', 'P4lastname', 'P4patientID']

# Step 3: check data (doubles, arrange) 
ad = pd.concat([od, nd], ignore_index=True)             # Concatenate old data and new data to check for doubles
ad['Patient'] = ['NL2', 'NL3', 'NL4', 'NL2','NL1',
                'NL4', 'NL3', 'NL6', 'NL7','NL1',
                'NL2', 'NL5', 'NL3', 'NL4','NL7','NL4'] # Tijdelijk voor anonieme data 

ad2 = ad.iloc[ad.astype(str).drop_duplicates().index]   # Drop doubles >> Return bool series to see which ones are double? 

ad3 = ad2.groupby(['Patient', 'MeasureDate']).sum()     # Arrange by patient ID and Measure date 

print(ad3)

# Write .XLSX-file 

