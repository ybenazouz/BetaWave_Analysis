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
import json                 # Import json module to process json files
import os                   # Import os module to create directories
import pathlib              # import Pathlib module to create directories
from tkinter import Tk      # Import tkinter module to create window in which a file can be selected
from tkinter.filedialog import askopenfilename      # Show window to select json file to be analyzed
# from datetime import date, datetime
import openpyxl 

# wb = load_workbook(filename=)
