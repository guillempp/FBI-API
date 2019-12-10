import requests
import json
from pandas import DataFrame
from pandas.io.json import json_normalize
from tkinter import *
import tkinter as tk

class FBIData:

    def __str__(self):
        return "ori: {},  data_year: {}, offense: {}, state_abbr: {}, cleared: {}, actual {}".format(str(self.ori), int(self.data_year), str(self.offense), str(self.state), int(self. cleared), int(self.actual))
    def __init__(self):
        self.api_key = "qcsfWTVg2DevXRBUoEAxeZA3jTlW6pHn0fohuUV4"

        self.offenses = ["aggravated-assault", "burglary", "larceny", "motor-vehicle-theft", "homicide", "rape", "robbery",
                         "arson", "violent-crime", "property-crime"]
        self.years = [2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018]
        self.states = {
            'AK': 'Alaska',
            'AL': 'Alabama',
            'AR': 'Arkansas',
            'AZ': 'Arizona',
            'CA': 'California',
            'CO': 'Colorado',
            'CT': 'Connecticut',
            'DC': 'District of Columbia',
            'DE': 'Delaware',
            'FL': 'Florida',
            'GA': 'Georgia',
            'HI': 'Hawaii',
            'IA': 'Iowa',
            'ID': 'Idaho',
            'IL': 'Illinois',
            'IN': 'Indiana',
            'KS': 'Kansas',
            'KY': 'Kentucky',
            'LA': 'Louisiana',
            'MA': 'Massachusetts',
            'MD': 'Maryland',
            'ME': 'Maine',
            'MI': 'Michigan',
            'MN': 'Minnesota',
            'MO': 'Missouri',
            'MS': 'Mississippi',
            'MT': 'Montana',
            'NC': 'North Carolina',
            'ND': 'North Dakota',
            'NE': 'Nebraska',
            'NH': 'New Hampshire',
            'NJ': 'New Jersey',
            'NM': 'New Mexico',
            'NV': 'Nevada',
            'NY': 'New York',
            'OH': 'Ohio',
            'OK': 'Oklahoma',
            'OR': 'Oregon',
            'PA': 'Pennsylvania',
            'RI': 'Rhode Island',
            'SC': 'South Carolina',
            'SD': 'South Dakota',
            'TN': 'Tennessee',
            'TX': 'Texas',
            'UT': 'Utah',
            'VA': 'Virginia',
            'VT': 'Vermont',
            'WA': 'Washington',
            'WI': 'Wisconsin',
            'WV': 'West Virginia',
            'WY': 'Wyoming'
        }

        self.options = ['age', 'ethnicity', 'race', 'sex']



    def getYears(self):
        return self.years
    def getStates(self):
        return self.states
    def getOffenses(self):
        return self.offenses
    def getApiKey(self):
        return self.api_key
    def getRegions(self):
        regions = []
        stateData = requests.get("https://api.usa.gov/crime/fbi/sapi/api/regions?api_key=tiq42dY2doj3mDPMG9B24q5bKsjjReClz2MnIdFE")
        stateJSON = json.loads(stateData.text)
        result = stateJSON["results"]
        for data in result:
            regions.append(data["region_name"])
        return regions

    def getOptions(self):
        return self.options

    def getData(self, userInput, option, stateAbbr):
        #State
        if option == 3:
            response = requests.get("https://api.usa.gov/crime/fbi/sapi/api/nibrs/{}/offense/states/{}/count?api_key={}".format(userInput, stateAbbr, self.getApiKey()))
        #National
        elif option == 1:
            response = requests.get("https://api.usa.gov/crime/fbi/sapi/api/nibrs/{}/offense/national/count?api_key={}".format(userInput, self.getApiKey()))
        #Region
        elif option == 2:
            response = requests.get("https://api.usa.gov/crime/fbi/sapi/api/nibrs/{}/offense/regions/{}/count?api_key={}".format(userInput, stateAbbr, self.getApiKey()))

        json_data = json.loads(response.text)
        #result = json_data["result"]
        processedData = []
        for data in json_data["data"]:
            processedData.append(data)
        #append in dataframe for graph
        return processedData

    def getProcessedData(self, yr, offense, stateAbbr, option, root):
        processedData2 = []
        
        #State
        if option == 3:

            response = requests.get("https://api.usa.gov/crime/fbi/sapi/api/nibrs/{}/offender/states/{}/age?API_KEY={}".format(offense, stateAbbr,self.getApiKey()))
            json_data = json.loads(response.text)
            keys = []
            dataforFrame = []
            data = json_normalize(json_data['data'])
            
            #processeddf = data.groupby('')
            processeddf = data.groupby('data_year')
            currentyear = processeddf.get_group(yr)
            currentyear.set_index('key', inplace=True)
            
            window = tk.Toplevel(root)
            window.minsize(1000, 600)
            frame = Frame(window)
            frame.grid(column=0, row=0, sticky=(N, W))
            frame.columnconfigure(0, weight=1)
            frame.rowconfigure(0, weight=1)
            frame.pack(pady=0, padx=0)
            
            Label(frame, text="Age group", width=10, pady=3, padx=3).grid(row=0, column = 1)
            Label(frame, text="Value", width=10, pady=3, padx=3).grid(row=0, column = 2)
            Label(frame, text="Data year", width=10, pady=3, padx=3).grid(row=0, column = 3)
            Label(frame, text="State Abbr", width=10, pady=3, padx=3).grid(row=0, column = 4)
            Label(frame, text="State Name", width=10, pady=3, padx=3).grid(row=0, column = 5)
            Label(frame, text="Offense", width=10, pady=3, padx=3).grid(row=0, column = 6)
            i = 1
            ind = 0
            getStates = self.getStates()
            for item in currentyear.index:
                Label(frame, text=currentyear.index[ind], width=10, pady=3, padx=3).grid(row=i, column = 1)
                Label(frame, text=currentyear['value'][ind], width=10, pady=3, padx=3).grid(row=i, column = 2)
                Label(frame, text=yr, width=10, pady=3, padx=3).grid(row=i, column = 3)
                Label(frame, text=stateAbbr, width=10, pady=3, padx=3).grid(row=i, column = 4)
                Label(frame, text=getStates[stateAbbr], width=10, pady=3, padx=3).grid(row=i, column = 5)
                Label(frame, text=offense, width=10, pady=3, padx=3).grid(row=i, column = 6)
                i+=1
                ind+=1
            def boom():
                window.destroy()
            button = tk.Button(window, text='Back', width=25, command =lambda: boom())
            button.pack()
        ###
        ### JUST WORKING WITH STATES
        ###
        
        #National
        elif option == 1:
            keys = []
            response = requests.get("https://api.usa.gov/crime/fbi/sapi/api/nibrs/{}/offender/national/age?API_KEY={}".format(offense, self.getApiKey()))
            json_data = json.loads(response.text)
            keys = []
            dataforFrame = []
            data = json_normalize(json_data['data'])
            
            #processeddf = data.groupby('')
            processeddf = data.groupby('data_year')
            currentyear = processeddf.get_group(yr)
            currentyear.set_index('key', inplace=True)
            
            window = tk.Toplevel(root)
            window.minsize(1000, 600)
            frame = Frame(window)
            frame.grid(column=0, row=0, sticky=(N, W))
            frame.columnconfigure(0, weight=1)
            frame.rowconfigure(0, weight=1)
            frame.pack(pady=0, padx=0)
            
            Label(frame, text="Age group", width=10, pady=3, padx=3).grid(row=0, column = 1)
            Label(frame, text="Value", width=10, pady=3, padx=3).grid(row=0, column = 2)
            Label(frame, text="Data year", width=10, pady=3, padx=3).grid(row=0, column = 3)
            Label(frame, text="State Abbr", width=10, pady=3, padx=3).grid(row=0, column = 4)
            Label(frame, text="State Name", width=10, pady=3, padx=3).grid(row=0, column = 5)
            Label(frame, text="Offense", width=10, pady=3, padx=3).grid(row=0, column = 6)
            i = 1
            ind = 0
            getStates = self.getStates()
            for item in currentyear.index:
                Label(frame, text=currentyear.index[ind], width=10, pady=3, padx=3).grid(row=i, column = 1)
                Label(frame, text=currentyear['value'][ind], width=10, pady=3, padx=3).grid(row=i, column = 2)
                Label(frame, text=yr, width=10, pady=3, padx=3).grid(row=i, column = 3)
                Label(frame, text="National", width=10, pady=3, padx=3).grid(row=i, column = 4)
                Label(frame, text="National", width=10, pady=3, padx=3).grid(row=i, column = 5)
                Label(frame, text=offense, width=10, pady=3, padx=3).grid(row=i, column = 6)
                i+=1
                ind+=1
            def boom():
                window.destroy()
            button = tk.Button(window, text='Back', width=25, command =lambda: boom())
            button.pack()
        #Region
        elif option == 2:
            response = requests.get("https://api.usa.gov/crime/fbi/sapi/api/nibrs/{}/offender/regions/{}/age?API_KEY={}".format(offense, stateAbbr, self.getApiKey()))
            json_data = json.loads(response.text)
            keys = []
            dataforFrame = []
            data = json_normalize(json_data['data'])
            
            #processeddf = data.groupby('')
            processeddf = data.groupby('data_year')
            currentyear = processeddf.get_group(yr)
            currentyear.set_index('key', inplace=True)
            
            window = tk.Toplevel(root)
            window.minsize(1000, 600)
            frame = Frame(window)
            frame.grid(column=0, row=0, sticky=(N, W))
            frame.columnconfigure(0, weight=1)
            frame.rowconfigure(0, weight=1)
            frame.pack(pady=0, padx=0)
            
            Label(frame, text="Age group", width=10, pady=3, padx=3).grid(row=0, column = 1)
            Label(frame, text="Value", width=10, pady=3, padx=3).grid(row=0, column = 2)
            Label(frame, text="Data year", width=10, pady=3, padx=3).grid(row=0, column = 3)
            Label(frame, text="State Abbr", width=10, pady=3, padx=3).grid(row=0, column = 4)
            Label(frame, text="State Name", width=10, pady=3, padx=3).grid(row=0, column = 5)
            Label(frame, text="Offense", width=10, pady=3, padx=3).grid(row=0, column = 6)
            i = 1
            ind = 0
            getStates = self.getStates()
            for item in currentyear.index:
                Label(frame, text=currentyear.index[ind], width=10, pady=3, padx=3).grid(row=i, column = 1)
                Label(frame, text=currentyear['value'][ind], width=10, pady=3, padx=3).grid(row=i, column = 2)
                Label(frame, text=yr, width=10, pady=3, padx=3).grid(row=i, column = 3)
                Label(frame, text=stateAbbr, width=10, pady=3, padx=3).grid(row=i, column = 4)
                Label(frame, text=stateAbbr, width=10, pady=3, padx=3).grid(row=i, column = 5)
                Label(frame, text=offense, width=10, pady=3, padx=3).grid(row=i, column = 6)
                i+=1
                ind+=1
            def boom():
                window.destroy()
            button = tk.Button(window, text='Back', width=25, command =lambda: boom())
            button.pack()
        
        return processedData2
