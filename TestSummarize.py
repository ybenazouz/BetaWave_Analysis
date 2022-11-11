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

# from loading_data import loading_data

# Stappenplan
# 1. xlsx downloaden met alle data 
# 2. xlsxl met sleutelbestand 
# 3. json bestanden selecteren en tellen hoe veel het er zijn
# 4. struct maken met goeie aantal rijen of kolommen 
# 5. loop starten, data er uit halen 
# 6. check de data met de data die er al in staat 
# 7. als niet dubbel voeg dan data toe 
# 8. report maken van wat wel en niet is toegevoegd???
# 9. anonymized json file uitgeven ook?? 

# Step 3: retrieve folder with files. 
Tk().withdraw()                 # we don't want a full GUI, so keep the root window from appearing
directory = askdirectory()      # show an "Open" dialog box and return the path to the selected directory 
                                # The directory should be a folder with JSON files you want to check and add to the xlsx. 

# Step 5: loop within folder to retrieve information
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        ## print(f)              # print current file path 
        data = json.load(open(f))

        # Date of download (in name)
        ## P01 = os.path.basename()   # Retrieve the directory
        ## P02 = os.path.splitext(P01)[0]      # select the filename in the directory

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

        # DeviceInformation: Date of Device Measurement and Type of Stimulator 
        MeasureDate = "Not available"       # not available unless available 
        StimulatorType = "Not available"    # not available unless available 
        if 'DeviceInformation' in data: 
            MeasureDate = data['DeviceInformation']['Final']['DeviceDateTime'].replace("T", " ").replace("Z", "")
            MeasureDate = datetime.strptime(MeasureDate, '%Y-%m-%d %H:%M:%S').date()
            StimulatorType = data['DeviceInformation']['Initial']['Neurostimulator']
        
            print(StimulatorType)
        # BatteryInformation
        # GroupUsagePercentage 
        # LeadConfiguration
        # Stimulation
        # Groups 
        # BatteryReminder 

        # BrainsenseSetup (sensechanneltests + calibrationtests)
        P6channel = []
        if "SenseChannelTests" in data:   # Check if SenseChannelTest is in data otherwise go to else
            try:    # When there is just one measurement no loop can be used and there for a try/except statement is used.
                for channel in data["SenseChannelTests"]:
                    P6channel.append(channel["Channel"])                    # Add al Channels to one list
                P6time = data["SenseChannelTests"][0]["FirstPacketDateTime"][0:19].replace("T", " ")        # Select datetime
                P6rec = len(data["SenseChannelTests"][0]["TimeDomainData"]) / data["SenseChannelTests"][0]["SampleRateInHz"]
                # Calculate the length of the recording
            
                P6 = f"BrainSense Setup Sense Channel Tests performed on channels:\n\t\t{P6channel}\n\t\tPerformed at {P6time}"
            except:
                P6channel = data["SenseChannelTests"]["Channel"]          # Select the channel and add to one list
                P6time = data["SenseChannelTests"][0]["FirstPacketDateTime"][0:19].replace("T", " ")    # Select the DateTime
                P6rec = len(data["SenseChannelTests"][0]["TimeDomainData"]) / data["SenseChannelTests"][0]["SampleRateInHz"]
                # Calculate the length of the recording
            
                P6 = f"BrainSense Setup Sense Channel Tests performed on channels:\n\t\t {P6channel}\n\t\tPerformed at {P6time}"
            else:
                P6 = "No BrainSense Setup Sense Channel Tests performed"          # If there is no SenseChannelTest in the data print this line.




