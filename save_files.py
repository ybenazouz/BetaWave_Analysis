"""
Function for Summarise3 Script 

save_files.py: Function that generates and saves 
    - An anonymized JSON- and TXT-file per patient in their personal folder. 
    - An updated Summarise .XLSX-file, with doubles removed. 
    - An archived .XLSX-file in the archived foler. 

(line 23) Step 1: Old data file to struct and new XLSX-file 
(line 35) Step 2: Load all new data from new_files folder
(line 48) Step 3: Check and remove doubles
(line 57) Step 4: Go over each row (patient) of new files to generate new files. 
(line 65) Step 4a: Create personal patient directory
(line 77) Step 4b: Create and save new .JSON-file 
(line 87) Step 4c: Write and save .TXT-file 
(line 171) Step 5: Write and save new general .XLSX-file

Author: 
Yasmin Ben Azouz
TM2 Intership 3, November 2022
Neurosurgery Department
Haga Hospital, The Hague 

"""
import json                 # Import json module to process json files
import os                   # Import os module to create directories
import pathlib              # import Pathlib module to create directories
import math as math
import pandas as pd
import numpy as np
from datetime import datetime

def save_files(new_data, directory):

    # Step 1: Old data file to struct and new XLSX-file
    od = pd.read_excel(                                             # Read the .xlsx file with old data as a panda datastruct
    pathlib.PurePath(directory, 'output.xlsx'))                     # Generate Path within Summarise folder to output file 
    if not od.empty: 
        od['MeasureDate'] = pd.to_datetime(od['MeasureDate']).dt.date   # Remove time from measuredate 

    old_name = 'Summarize3_archived_' +str(datetime.now().strftime("%Y-%m-%d %H.%M") )+ '.xlsx'  # Generate new name for old file that will be archived
    archive = pathlib.PurePath(directory, 'Archive')                # Generate Path within Summarise folder to Archive folder 
    od.to_excel(                                                    # Generate new .xlsx file for archive and add to archive folder
    pathlib.PurePath(archive, old_name))                            # Generate new .xlsx file for archive and add to archive folder

    # Step 2: Load all new data from new_files folder
    nd = pd.DataFrame(new_data)                                     # Turn list with all data to datastruct
    nd.columns = ['Patient','MeasureDate', 'StimulatorType', 
        'P6channel', 'P6rec', 'P6time',
        'P7channel', 'P7rec', 'P7time',
        'P11channel', 'P11rec', 'P11time', 'P11time2',
        'P2channel', 'P2rec', 'P2time',
        'P1DateTime', 
        'P3DateEnd', 'P3DateStart', 'P3Days', 'P3end', 'P3start', 
        'P9Events',
        'Filename']

    # Step 3: Check and remove doubles
    ad = pd.concat([od, nd], ignore_index=True)             # Concatenate old data and new data to check for doubles
    ad['Patient'] = ['NL2', 'NL3', 'NL4', 'NL2','NL1',
            'NL4', 'NL3', 'NL6', 'NL7','NL1',
            'NL2', 'NL5', 'NL3', 'NL4','NL7'] # Tijdelijk voor anonieme data een ID geven.

    ad2 = ad.iloc[ad.astype(str).drop_duplicates().index]   # Drop doubles >> Return bool series to see which ones are double? 

    # Step 4: Go over each row (patient) of new files to generate new files. 
    for index, row in ad2.iterrows():
        filename = row['Filename'] 
        if not pd.isnull(filename): 
            Patient = row['Patient']
  
            # Step 4a: Create personal patient directory
            pat_dir = pathlib.PurePath(directory,'Patients', Patient) 
            try:
                os.makedirs(pat_dir)
            except FileExistsError:
                pass

            directory_json = pathlib.PurePath(directory, 'new_files')       # Directory to folder with new .JSON-files
            f = pathlib.PurePath(directory_json, filename)
            data = json.load(open(f))

            # Step 4b: Create new .JSON-file 
            data_anon = data 
            data_anon["PatientInformation"] = Patient 
            filename_anon = filename.replace('.json', '')+'_anonymous.json'

            json_name = pathlib.PurePath(pat_dir, filename_anon)
            with open(json_name, "w") as j:
                json.dump(data_anon, j) 

            # Step 4c: Write .TXT-file 
            filename_txt = filename.replace('.json', '')+'.txt'
            txt_name = pathlib.PurePath(pat_dir, filename_txt)
            
            P3 = f"No EventSummary available"
            if not pd.isnull(row['P3start']): 
                P3 = f"EventSummary for timeline started at {row['P3start']} and ended at {row['P3end']} (Total of {row['P3Days']} days)"

            P9 = f"No events registered by patient"
            if not pd.isnull(row['P9Events']):
                P9 = f"Number of events registered by patient: {row['P9Events']}"

            P1 = "No BrainSense Streaming (LFP) measurement performed" 
            if not np.all(pd.isnull(row['P1DateTime'])):
                P1 = f"BrainSense Streaming (LFP) performed at:\n\t\t{row['P1DateTime']}"          
            
            P2 = "No BrainSense Survey Recording (IndefiniteStreaming) measurement performed" 
            if not np.all(pd.isnull(row['P2channel'])):
                P2 = f"BrainSense Survey Recording (IndefiniteStreaming) performed on channels:\n\t\t{row['P2channel']}\n\t\tPerformed at {row['P2time']} for {row['P2rec']} seconds"

            P11 = "No BrainSense Survey LFP measurement performed" 
            if not np.all(pd.isnull(row['P11channel'])):
                        P11 = f"BrainSense Survey LFP measurement performed on channels:\n\t\t{row['P11channel']}\n\t\tPerformed between {row['P11time']} and {row['P11time2']}"

            P7 = "No BrainSense Setup Calibration Tests performed" 
            if not np.all(pd.isnull(row['P7channel'])): 
                P7 = f"BrainSense Setup Calibration Tests performed on channels:\n\t\t{row['P7channel']}\n\t\tPerformed at {row['P7time']}"

            P6 = "No BrainSense Setup Sense Channel Tests performed" 
            if not np.all(pd.isnull(row['P6channel'])): 
                P6 = f"BrainSense Setup Sense Channel Tests performed on channels:\n\t\t {row['P6channel']}\n\t\tPerformed at {row['P6time']}"

            # Merge numbers in filename 
            P0 = filename.split('_')                 # split the filename based on underscores
            P0[0:2] = ['_'.join(P0[0:2])]       # Merge two parts of the patients anonymous ID 

            # Date of download (in name)
            Year = P0[-1][0:4]                  # select the year in the Filename
            Month = P0[-1][4:6]                 # select the month in the Filename
            Day = P0[-1][6:8]                   # select the day in the Filename

            Hour = P0[-1][9:11]                 # select the hour in the Filename
            Minute = P0[-1][11:13]              # select the minute in the Filename
            Second = P0[-1][13:15]              # select the day in the Filename

            with open(txt_name, "w+") as t:
                t.write(
                    f"General file information:\n"
                    "\n"
                    f"\tPatient ID: {row['Patient']}\n"
                    "\n"
                    f"\tDate of measurement: {row['MeasureDate']}\n"
                    "\n"
                    "\n"
                    f"In-office measurements performed are:\n"
                    "\n"
                    f"\tBrainSense Setup"
                    "\n"
                    f"\t\t{P6}\n"           # SenseChannelTest measurements
                    "\n"
                    f"\t\t{P7}\n"           # CalibrationTest measurements
                    "\n"
                    f"\tBrainSense Survey"
                    "\n"
                    f"\t\t{P11}\n"          # LFPmontageTimeDomain measurements
                    "\n"
                    f"\t\t{P2}\n"           # IndefiniteStreaming measurements
                    "\n"
                    f"\tBrainSense Streaming"
                    "\n"
                    f"\t\t{P1}\n"           # BrainSenseLfp measurements
                    "\n"
                    "\n"
                    "Home measurements performed are:\n"
                    "\n"
                    f"\t{P3}\n"          # Event summary
                    "\n"
                    f"\t{P9}\n"           # Amount of events
                    "\n"
                    "\n"
                    f"(Measurement downloaded on {Year}-{Month}-{Day} at {Hour}:{Minute}:{Second})\n") 
                t.close()

    # Step 5: Write new general .XLSX-file 
    ad3 = ad2.groupby(['Patient'], observed=True, dropna=False)#.sum()     # Arrange by patient ID and Measure date 
    print(ad3)
    #dir_xlsx = pathlib.PurePath(directory, 'nieuwe_output.xlsx')
    #with open(dir_xlsx, "w+") as x: 
        #ad3.to_excel(dir_xlsx)

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    # writer = pd.ExcelWriter('nieuwe_output.xlsx', engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    # ad3.to_excel(writer, sheet_name='Sheet1')

    # Close the Pandas Excel writer and output the Excel file.
    # writer.save()
    return()