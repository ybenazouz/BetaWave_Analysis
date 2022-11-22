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
- pip install xlsxwriter 
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
from save_files import save_files

import numpy as np

# from loading_data import loading_data

# Step 1: retrieve folder with all summarise3 information 
Tk().withdraw()                         # prevent full GUI
dir_sum = askdirectory()                # Show an "Open" dialog box and return the path to the selected directory 
                                        # Summarise3 folder
# Old Data 
od = pd.read_excel(pathlib.PurePath(dir_sum, 'output.xlsx'))    # read the .xlsx file as a panda datastruct 
if not od.empty: 
    od['MeasureDate'] = pd.to_datetime(od['MeasureDate']).dt.date   # remove time from measuredate 

old_name = 'Summarize3_archived_' +str(datetime.now().strftime("%Y-%m-%d %H.%M") )+ '.xlsx'  # Generate new name for old file that will be archived
archive = pathlib.PurePath(dir_sum, 'Archive')              # generate Path to archive 
od.to_excel(pathlib.PurePath(archive, old_name))            # Generate new .xlsx file for archive and add to archive folder

# Anonymization Key 
anon = pd.read_excel(pathlib.PurePath(dir_sum, 'Anonymisation.xlsx'))    # read the .xlsx file as a panda datastruct 
 
directory_json = pathlib.PurePath(dir_sum, 'new_files')   

new_data, data = open_json(directory_json, anon)

save_files(new_data, od, dir_sum, directory_json)

