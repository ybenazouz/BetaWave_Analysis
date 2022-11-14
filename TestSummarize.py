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

# Import selfmade functions 
from open_json import open_json

# from loading_data import loading_data

# Stappenplan
# 1. xlsx downloaden met alle data 
# 2. xlsxl met sleutelbestand 
# 3. json bestanden selecteren en tellen hoe veel het er zijn
# 5. loop starten, data er uit halen 
# 6. check de data met de data die er al in staat 
# 7. als niet dubbel voeg dan data toe 
# 8. report maken van wat wel en niet is toegevoegd???
# 9. anonymized json file uitgeven ook?? 

# Step 1: retrieve .xlsx with all information. 
Tk().withdraw()                 # we don't want a full GUI, so keep the root window from appearing
directory_excel = askopenfilename()      # show an "Open" dialog box and return the path to the selected directory 

od = pd.read_excel(directory_excel)     # Load old data into dataframe 

od['MeasureDate'] = pd.to_datetime(od['MeasureDate']).dt.date
# print(od)

# Step 2: retrieve .xlsx with anonymization key. 
## Tk().withdraw()                 # we don't want a full GUI, so keep the root window from appearing
## directory_anon = askopenfilename()      # show an "Open" dialog box and return the path to the selected directory 

## anon = pd.read_excel(directory_anon)    # read the .xlsx file as a panda datastruct 

## pat_id = anon.loc[:,"Patient ID"]       # retrieve the patient id's from the data stuct 
## pat_name = anon.loc[:,"Patient Name"]   # retieve the patient names from the data struct 
## pat = anon.loc[:,"Patient Number"]      # retrieve replacement patient number

# Step 3: retrieve folder with files. 
Tk().withdraw()                 # we don't want a full GUI, so keep the root window from appearing
directory_json = askdirectory() # show an "Open" dialog box and return the path to the selected directory 
                                # The directory should be a folder with JSON files you want to check and add to the xlsx.
                                 
# Step 4: loop within folder to retrieve information and put in struct
new_data = []                   # Create list to append lists with data to
for filename in os.listdir(directory_json):
    if filename !='.DS_Store':  # Hidden files in macbooks. 
    # open_json function >> is het handiger de if loop hiervoor te beginnen? Zit er nu in? Of vanaf data? 
        list = open_json(directory_json, filename)
        new_data.append(list)
## print(new_data)

nd = pd.DataFrame(new_data)     # Turn list with all data to datastruct
nd.columns = ['MeasureDate', 'StimulatorType', 
        'P6channel', 'P6rec', 'P6time',
        'P7channel', 'P7rec', 'P7time',
        'P11channel', 'P11rec', 'P11time', 'P11time2',
        'P2channel', 'P2rec', 'P2time',
        'P1DateTime', 
        'P3DateEnd', 'P3DateStart', 'P3Days', 'P3end', 'P3start', 
        'P9Events', 
        'P4firstname', 'P4lastname', 'P4patientID']
## print(nd)
## nd.to_excel("output.xlsx") 

# Step 5: check data for doubles 
ad = pd.concat([od, nd], ignore_index=True) # Concatenate old data and new data to check for doubles
print(ad['P3Days'])

dd = ad.drop(['P6channel', 'P7channel', 'P11channel', 'P2channel'], axis=1)
ad = ad.drop([1, 2])
print(ad)

bs = ad['StimulatorType'].astype(str).duplicated()
bs2 = ad['P6channel'].astype(str).duplicated()
bs3 = ad['P6rec'].astype(str).duplicated()
bs4 = ad['P6time'].astype(str).duplicated()
bs5 = ad['P7channel'].astype(str).duplicated()
bs8 = ad['P7rec'].astype(str).duplicated()
bs9 = ad['P7time'].astype(str).duplicated()
bs10 = ad['P11channel'].astype(str).duplicated()
bs11 = ad['P11rec'].astype(str).duplicated()
bs12 = ad['P11time'].astype(str).duplicated()
bs13 = ad['P11time2'].astype(str).duplicated()
bs14 = ad['P2channel'].astype(str).duplicated()
bs15 = ad['P2rec'].astype(str).duplicated()
bs16 = ad['P2time'].astype(str).duplicated()
bs17 = ad['P1DateTime'].astype(str).duplicated()
bs18 = ad['P3DateEnd'].astype(str).duplicated()
bs19 = ad['P3DateStart'].astype(str).duplicated()
bs20 = ad['P3Days'].astype(str).duplicated()
bs21 = ad['P3end'].astype(str).duplicated()
bs22 = ad['P3start'].astype(str).duplicated()
bs23 = ad['P9Events'].astype(str).duplicated()
print(bs,bs2,bs3,bs4,bs5,bs8,bs9,bs10,bs11,bs12,bs13,bs14,bs15,bs16,bs17,bs18,bs19,bs20,bs21,bs22, bs23)
        #'P4firstname', 'P4lastname', 'P4patientID'].astype(str).duplicated() #drop_duplicates().index]
# bool_series = ad.duplicated() #(keep='first')   # Remove duplicates
## pd.set_option('display.max_columns', None)
## ad.head()
dd2 = dd.iloc[ad.astype(str).drop_duplicates().index]

#print(bool_series)
## print(ad['P7time'].to_string(index=False))
print(dd2)


