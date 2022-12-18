"""
Summarise3 Script: Python script to anonymize and store data from JSon files of patients with DBS. 

(line 38) Step 1: Retrieve path to Summarise3 folder.
(line 44) Step 2: Use open_json.py function 
(line 48) Step 3: Use save_files.py functon 

Input: 
    - Summarise Folder (contents of the Summarise folder are detailed in report (Y. Ben Azouz)). 

Output: 
    - An anonymized JSON- and TXT-file per patient in their personal folder. 
    - An updated Summarise .XLSX-file, with doubles removed. 
    - An archived .XLSX-file in the archived foler. 
Author: 
Yasmin Ben Azouz
TM2 Intership 3, November 2022
Neurosurgery Department
Haga Hospital, The Hague 

Modules to download before using the code: 
- pip install openpyxl
- pip install xlsxwriter 
"""
# Imports 
import pathlib                          # import Pathlib module to create directories
from datetime import datetime
from tkinter import \
    Tk                                  # Import tkinter module to create window in which a file can be selected
from tkinter.filedialog import \
    askdirectory                        # Show window to select json file to be analyzed
import pandas as pd
import math as math 

# Import selfmade functions 
from open_json import open_json         
from save_files import save_files

# Step 1: Retrieve path to Summarise3 folder.  
Tk().withdraw()                         # prevent full GUI
dir_sum = askdirectory()                # Show an "Open" dialog box and return the path to the selected directory Summarise3 folder
                         
# Step 2: Use open_json.py function 
new_data = open_json(dir_sum)

# Step 3: Use save_files.py functon 
save_files(new_data, dir_sum)

