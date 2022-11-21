"""
Python script to anonymize and store data from JSon files of patients with DBS. 
Data extracted from the json files by means of the Summarize2.py app will be put accordingly into the main excel sheet.
The data will also be anonymized, using a anonymization key. 

Author: 
Yasmin Ben Azouz
TM2 Intership 3
Neurosurgery Department
Haga Hospital, The Hague 

"""
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
import math as math

def open_json(directory, filename, anonymisation_key):
    anon = anonymisation_key
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
        MeasureDate = f"Not available"       # not available unless available 
        StimulatorType = f"Not available"    # not available unless available 
        if 'DeviceInformation' in data: 
            MeasureDate = data['DeviceInformation']['Final']['DeviceDateTime'].replace("T", " ").replace("Z", "")
            MeasureDate = datetime.strptime(MeasureDate, '%Y-%m-%d %H:%M:%S').date()
            StimulatorType = data['DeviceInformation']['Initial']['Neurostimulator']
        
            ## print(StimulatorType)
        # BatteryInformation
        # GroupUsagePercentage 
        # LeadConfiguration
        # Stimulation
        # Groups 
        # BatteryReminder 

        # BrainsenseSetup (sensechanneltests + calibrationtests)
        P6channel = []
        P6rec = []
        P6time = []
        if "SenseChannelTests" in data:   # Check if SenseChannelTest is in data otherwise go to else
            try:    # When there is just one measurement no loop can be used and there for a try/except statement is used.
                for channel in data["SenseChannelTests"]:
                    P6channel.append(str(channel["Channel"]))                    # Add al Channels to one list
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
            P6channel = float('nan')
            P6rec = float('nan')
            P6time = float('nan')

        P7channel = []
        if "CalibrationTests" in data:   # Check if CalibrationTest is in data otherwise go to else
            try:    # When there is just one measurement no loop can be used and there for a try/except statement is used.
                for channel in data["CalibrationTests"]:
                    P7channel.append(str(channel["Channel"]))                    # Add al Channels to one list
                P7time = data["CalibrationTests"][0]["FirstPacketDateTime"][0:19].replace("T", " ")        # Select datetime
                P7rec = len(data["CalibrationTests"][0]["TimeDomainData"]) / data["CalibrationTests"][0]["SampleRateInHz"]
                # Calculate the length of the recording
                
                P7 = f"BrainSense Setup Calibration Tests performed on channels:\n\t\t{P7channel}\n\t\tPerformed at {P7time}"
            except:
                P7channel = data["CalibrationTests"]["Channel"]          # Select the channel and add to one list
                P7time = data["CalibrationTests"][0]["FirstPacketDateTime"][0:19].replace("T", " ")    # Select the DateTime
                P7rec = len(data["CalibrationTests"][0]["TimeDomainData"]) / data["CalibrationTests"][0]["SampleRateInHz"]
                # Calculate the length of the recording
                
                P7 = f"BrainSense Setup Calibration Tests performed on channels:\n\t\t{P7channel}\n\t\tPerformed at {P7time}"
        else:
            P7 = "No BrainSense Setup Calibration Tests performed"          # If there is no SenseChannelTest in the data print this line.
            P7channel = float('nan')
            P7rec = float('nan')
            P7time = float('nan')

        # Brainsense Survey (LFPmontage (time domain))
        P11channel = []
        if "LfpMontageTimeDomain" in data:   # Check if LfpMontageTimeDomain is in data otherwise go to else
            try:    # When there is just one measurement no loop can be used and there for a try/except statement is used.
                for channel in data["LfpMontageTimeDomain"]:
                    P11channel.append(str(channel["Channel"]))                    # Add al Channels to one list
                P11time = data["LfpMontageTimeDomain"][0]["FirstPacketDateTime"][0:19].replace("T", " ")        # Select datetime
                P11time2 = data["LfpMontageTimeDomain"][-1]["FirstPacketDateTime"][0:19].replace("T", " ") 
                P11rec = len(data["LfpMontageTimeDomain"][0]["TimeDomainData"]) / data["LfpMontageTimeDomain"][0]["SampleRateInHz"]
                # Calculate the length of the recording

                P11 = f"BrainSense Survey LFP measurement performed on channels:\n\t\t{P11channel}\n\t\tPerformed between {P11time} and {P11time2}"
            except:
                P11channel = data["LfpMontageTimeDomain"]["Channel"]          # Select the channel and add to one list
                P11time = data["LfpMontageTimeDomain"][0]["FirstPacketDateTime"][0:19].replace("T", " ")    # Select the DateTime
                P11time2 = data["LfpMontageTimeDomain"][-1]["FirstPacketDateTime"][0:19].replace("T", " ")    # Select the DateTime
                P11rec = len(data["LfpMontageTimeDomain"][0]["TimeDomainData"]) / data["LfpMontageTimeDomain"][0]["SampleRateInHz"]
                # Calculate the length of the recording

                P11 = f"BrainSense Survey LFP measurement performed on channels:\n\t\t{P11channel}\n\t\tPerformed between {P11time} and {P11time2}"
        else:
            P11 = "No BrainSense Survey LFP measurement performed"          # If there is no IndefiniteStreaming in the data print this line.
            P11channel = float('nan') 
            P11rec = float('nan') 
            P11time = float('nan') 
            P11time2 = float('nan')

        # BrainSense Survey Recording (IndefiniteStreaming)
        P2channel = []
        if "IndefiniteStreaming" in data:   # Check if IndefiniteStreaming is in data otherwise go to else
            try:    # When there is just one measurement no loop can be used and there for a try/except statement is used.
                for channel in data["IndefiniteStreaming"]:
                    P2channel.append(str(channel["Channel"]))                    # Add al Channels to one list
                P2time = data["IndefiniteStreaming"][0]["FirstPacketDateTime"][0:19].replace("T", " ")        # Select datetime
                P2rec = len(data["IndefiniteStreaming"][0]["TimeDomainData"]) / data["IndefiniteStreaming"][0]["SampleRateInHz"]
                # Calculate the length of the recording

                P2 = f"BrainSense Survey Recording (IndefiniteStreaming) performed on channels:\n\t\t{P2channel}\n\t\tPerformed at {P2time} for {P2rec} seconds"
            except:
                P2channel = data["IndefiniteStreaming"]["Channel"]          # Select the channel and add to one list
                P2time = data["IndefiniteStreaming"][0]["FirstPacketDateTime"][0:19].replace("T", " ")    # Select the DateTime
                P2rec = len(data["IndefiniteStreaming"][0]["TimeDomainData"]) / data["IndefiniteStreaming"][0]["SampleRateInHz"]
                # Calculate the length of the recording

                P2 = f"BrainSense Survey Recording (IndefiniteStreaming) performed on channels:\n\t\t{P2channel}\n\t\tPerformed at {P2time} for {P2rec} seconds"
        else:
            P2 = "No BrainSense Survey Recording (IndefiniteStreaming) measurement performed"          # If there is no IndefiniteStreaming in the data print this line.
            P2channel = float('nan') 
            P2rec = float('nan') 
            P2time = float('nan')

        # BrainSense Streaming (LFP)
        P1DateTime = []
        if 'BrainSenseLfp' in data:         # Check if BrainSenseLfp is in data otherwise go to else
            try:       # When there is just one measurement no loop can be used and there for a try/except statement is used.
                for time in data['BrainSenseLfp']:
                    P1DateTime.append(time['FirstPacketDateTime'][0:19].replace("T", " "))    # Add all DateTimes to one list
                P1 = f"BrainSense Streaming (LFP) performed at:\n\t\t{P1DateTime}"           # Create sentence which is printed to the txtfile
            except:
                P1DateTime = data['BrainSenseLfp']['FirstPacketDateTime'][0:19].replace("T", " ")
                P1 = f"BrainSense Streaming (LFP) performed at:\n\t\t{P1DateTime}"           # Create sentence which is printed to the txtfile
        else:
            P1 = "No BrainSense Streaming (LFP) measurement performed"       # When BrainSenseLfp is not in data print this line to txtfile
            P1DateTime = float('nan')

        # BrainSense Timeline / Events (EventSummary) --> toevoegen aantal events!
        P3 = []
        if "EventSummary" in data:                  # Check if EvenSummary is in the data.
            P3start = data["EventSummary"]["SessionStartDate"][0:19].replace("T", " ")        # Select the start of the session
            P3end = data["EventSummary"]["SessionEndDate"][0:19].replace("T", " ")            # Select the end of the session
            P3DateStart = date(int(P3start[0:4]), int(P3start[5:7]), int(P3start[8:10]))
            P3DateEnd = date(int(P3end[0:4]), int(P3end[5:7]), int(P3end[8:10]))
            P3delta = P3DateEnd - P3DateStart
            P3Days = P3delta.days
            P3 = f"EventSummary for timeline started at {P3start} and ended at {P3end} (Total of {P3Days} days)"  # Print this line
        else:
            P3 = "No EventSummary available"
            P3DateEnd = float('nan') 
            P3DateStart = float('nan') 
            P3Days = float('nan') 
            P3end = float('nan') 
            P3start = float('nan') 

        P9 = []
        if "DiagnosticData" in data and "LfpFrequencySnapshotEvents" in data["DiagnosticData"]:
            P9Events = len(data["DiagnosticData"]["LfpFrequencySnapshotEvents"])
            P9 = f"Number of events registered by patient: {P9Events}"
        else:
            P9 = f"No events registered by patient"
            P9Events = float('nan')

        # Patient information
        P4 = []
        P5 = []
        if "PatientInformation" in data and "Final" in data["PatientInformation"]:
            P4firstname = data["PatientInformation"]["Final"]["PatientFirstName"]
            P4lastname = data["PatientInformation"]["Final"]["PatientLastName"]
            P4patientID = data["PatientInformation"]["Final"]["PatientId"]
            P4 = f"{P4firstname} {P4lastname}"
            P5 = f"{P4patientID}"
            if not P5:
                P5 = f"Not provided"
        else:
            P4 = f"File is anonymized, anonymize ID is: {filename}"
            P5 = "File is anonymized, Patient ID not available"
            P4firstname = float('nan') 
            P4lastname = float('nan') 
            P4patientID = float('nan')

        # Anonymize + arrange 
        Patient = [] # create studt 
        for index, row in anon.iterrows():  # Loop through key information 
            if not math.isnan(row['ID']):
                # ook if anon is float vlaue voor omzetten integer? maakt dat uit? 
                id = math.floor(row['ID']) # turn float patient id into integer using numpy series   
                if id == P4patientID : 
                    Patient = row['Pseudo']
            elif row['LastName'] == P4lastname:
                Patient = row['Pseudo']   
        else: 
            Patient = 'Unknown'   
            # controle of anon_id even lang is als het aantal rijen in pid? 
            # Controleren of er unknown identity staat etc? 
            # Controleren of het een onbekende patient naam en id is? In dit geval melding geven om toe te voegen in de key?      
    #print(anon_id)

        # Create list for patient with all values
        list = [Patient, MeasureDate, StimulatorType, 
        P6channel, P6rec, P6time,
        P7channel, P7rec, P7time,
        P11channel, P11rec, P11time, P11time2,
        P2channel, P2rec, P2time,
        P1DateTime, 
        P3DateEnd, P3DateStart, P3Days, P3end, P3start, 
        P9Events, 
        P4firstname, P4lastname, P4patientID]
    return(list)

### create text file
