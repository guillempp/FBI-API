from tkinter import *
import tkinter as tk
from pandas import DataFrame
from FBIDATA import FBIData
from plot import plot

class RunProgram:

    global shows
    shows = False
    def __init__(self):
        self.GUI2()


    ###


    ### NEW IMPLEMENTATION


    ###

    ###
    ### Passes var1 = offense
    ### var2 = option (national, state or region)
    ### var3 = state Abbre, will return "States" if National is chosen and then regions or states
    ### yr initial year
    ### end year
    ###
    
    
    ### Repopulate frame function
    def RepopulateFrame(self, mainframe, var1, var2, var3, yr, eyr):
    
        appear = True
        root = Tk()
        root.title("FBI API")
        root.minsize(1000, 600)

        #Add a grid
        mainframe = Frame(root)
        mainframe.grid(column=0, row=0, sticky=(N, W))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        mainframe.pack(pady=0, padx=0)
            
        ### Run query and append data to dataframe.
        def runQuery(var1, var2, var3, yr, eyr):
            data = FBIData().getData(var1, var2, var3)
            stateAbbr = FBIData().getStates()
            df1 = DataFrame(data, columns=['data_year', 'value'])
            df1 = df1[['data_year', 'value']].groupby('data_year').sum()
            i=1
            yrs = abs(int(yr) - int(eyr))
            yin = int(yr)
            Label(mainframe, text="Value", width=10, pady=3, padx=3).grid(row=0, column = 2)
            Label(mainframe, text="Data year", width=10, pady=3, padx=3).grid(row=0, column = 3)
            Label(mainframe, text="State Abbr", width=10, pady=3, padx=3).grid(row=0, column = 4)
            Label(mainframe, text="State Name", width=10, pady=3, padx=3).grid(row=0, column = 5)
            Label(mainframe, text="Offense", width=10, pady=3, padx=3).grid(row=0, column = 6)
            btns = {}
            if var2 == 1:
                for item in range((yrs+1)):
                    year = df1.loc[yin]
                    Label(mainframe, text=year['value'], width=10, pady=3, padx=3).grid(row=i, column = 2)
                    Label(mainframe, text=yin, width=10, pady=3, padx=3).grid(row=i, column = 3)
                    Label(mainframe, text="National", width=10, pady=3, padx=3).grid(row=i, column = 4)
                    Label(mainframe, text="National", width=10, pady=3, padx=5).grid(row=i, column = 5)
                    Label(mainframe, text=var1, width=10, pady=3, padx=3).grid(row=i, column = 6)
                    b = Button(mainframe, text="More info", width=10, command =lambda yin=yin: moreInfo(yin, var1, var3, var2))
                    b.grid(row=i, column=1)
                    i+=1
                    yin+=1
            elif var2 == 2:
                regions = FBIData().getRegions()
                for item in range((yrs+1)):
                    year = df1.loc[yin]
                    Label(mainframe, text=year['value'], width=10, pady=3, padx=3).grid(row=i, column = 2)
                    Label(mainframe, text=yin, width=10, pady=3, padx=3).grid(row=i, column = 3)
                    Label(mainframe, text=var3, width=10, pady=3, padx=3).grid(row=i, column = 4)
                    Label(mainframe, text=var3, width=10, pady=3, padx=5).grid(row=i, column = 5)
                    Label(mainframe, text=var1, width=10, pady=3, padx=3).grid(row=i, column = 6)
                    b = Button(mainframe, text="More info", width=10, command =lambda yin=yin: moreInfo(yin, var1, var3, var2))
                    b.grid(row=i, column=1)
                    i+=1
                    yin+=1
            elif var2 == 3:
                for item in range((yrs+1)):
                    year = df1.loc[yin]
                    Label(mainframe, text=year['value'], width=10, pady=3, padx=3).grid(row=i, column = 2)
                    Label(mainframe, text=yin, width=10, pady=3, padx=3).grid(row=i, column = 3)
                    Label(mainframe, text=var3, width=10, pady=3, padx=3).grid(row=i, column = 4)
                    Label(mainframe, text=stateAbbr[var3], width=10, pady=3, padx=5).grid(row=i, column = 5)
                    Label(mainframe, text=var1, width=10, pady=3, padx=3).grid(row=i, column = 6)
                    b = Button(mainframe, text="More info", width=10, command =lambda yin=yin: moreInfo(yin, var1, var3, var2))
                    b.grid(row=i, column=1)
                    i+=1
                    yin+=1

        runQuery(var1, var2, var3, yr, eyr)
        
        ### Run query for graphing.
        def rerunQuery():
            data = FBIData().getData(var1, var2, var3)
            df1 = DataFrame(data, columns=['data_year', 'value'])
            df1 = df1[['data_year', 'value']].groupby('data_year').sum()
            year = df1.loc[int(yr):int(eyr)]
            return year
            
        def moreInfo(yr, offense, stateAbbr, option):
            df1 = FBIData().getProcessedData(yr, offense, stateAbbr,  option, root)

        b = tk.Button(root, text="Graph", width=25, command =lambda: plot.plot1(self, rerunQuery(), mainframe, var3, var1, int(yr), int(eyr)))
        b.pack()
        
        #Destroy frame
        def boom():
            root.destroy()
            mainframe.destroy()
            self.GUI2()
        button = tk.Button(root, text='Back', width=25, command =lambda: boom())
        button.pack()

        root.mainloop()


    #Called GUI2 to support different implementation, works now so far.
    def GUI2(self):
        appear = True
        root = Tk()
        root.title("FBI API")
        root.minsize(600, 300)
        #Add a grid
        mainframe = Frame(root)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        mainframe.pack(pady=0, padx=0)

        v = IntVar(root)
        national = Radiobutton(root, text='National', variable=v, value=1).pack()
        regions = Radiobutton(root, text='Regional', variable=v, value=2).pack()
        state = Radiobutton(root, text='State', variable=v, value=3)
        state.pack()
        state.select()



        # Create a Tkinter variable
        tkvar = StringVar(root)
        tkvar2 = StringVar(root)

        choices = []
        #set states as default
        for off in FBIData().getStates().keys():
            choices.append(off)
        tkvar.set("States")
        popupMenu = OptionMenu(mainframe, tkvar, *choices)
        popupMenu.grid(row=1, column=1)


        def changedOption(*args):
            choices = []
            if v.get() == 1:
                tkvar.set("National")
                popupMenu.configure(state="disabled")
            elif v.get() == 2:
                choices = []
                tkvar.set("Regional")
                choices = FBIData().getRegions()
                m = popupMenu.children["menu"]
                m.delete(0, END)
                for choice in choices:
                    m.add_command(label=choice, command=lambda v=tkvar, l=choice: v.set(l))
                popupMenu.configure(state="active")
                #popupMenu = OptionMenu(mainframe, tkvar, *choices)
                #popupMenu.grid(row=1, column=1)
            elif v.get() == 3:
                tkvar.set("State")
                appear = True
                for off in FBIData().getStates().keys():
                    choices.append(off)
                m = popupMenu.children["menu"]
                m.delete(0, END)
                for choice in choices:
                    m.add_command(label=choice, command=lambda v=tkvar, l=choice: v.set(l))
                popupMenu.configure(state="active")
                #popupMenu = OptionMenu(mainframe, tkvar, *choices)
                #popupMenu.grid(row=1, column=1)
            else:
                tkvar.set("Select a value")

        #create second dropdown
        tkvar2.set("Offense")
        dropdown2 = OptionMenu(mainframe, tkvar2, *FBIData().getOffenses())
        dropdown2.grid(row=1,column=2)

        # Add plot and data
        #Figure out how to change and update graph

        #Start year
        tkvar3 = StringVar(root)
        tkvar3.set("Start Year")
        dropdown2 = OptionMenu(mainframe, tkvar3, *FBIData().getYears())
        dropdown2.grid(row=1,column=3)
        #End year
        tkvar4 = StringVar(root)
        tkvar4.set("End Year")
        dropdown3 = OptionMenu(mainframe, tkvar4, *FBIData().getYears())
        dropdown3.grid(row=1,column=4)
        
        button = tk.Button(root, text='Search', width=25, command =lambda: self.RepopulateFrame(mainframe, tkvar2.get(), v.get(), tkvar.get(), tkvar3.get(), tkvar4.get()))
        button.pack()
        
        button.config(state='disabled')
        
        
        def disableButton(*args):
            tk4 = tkvar4.get()
            
            if tk4:
                button.config(state='active')
            else:
                button.config(state='disabled')
                
        v.trace('w', changedOption)
        tkvar4.trace_variable('w', disableButton)


        root.mainloop()


RunProgram()
