import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame
from tkinter import *
import tkinter as tk

class plot:
        
    def plot1(self, df1, mainframe, state, offense, yr, eyr):
        appear = True
        root = Tk()
        root.title("FBI API")
        #Add a grid
        mainframe = Frame(root)
        mainframe.grid(column=0, row=0, sticky=(N, W))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        
        mainframe.pack(pady=0, padx=0)
        
        self.figure, self.ax = plt.subplots(nrows=1, ncols=1)
        chart_type = FigureCanvasTkAgg(self.figure, root)
        chart_type.get_tk_widget().pack()

        df1.plot(kind='bar', legend=True,ax=self.ax);

        self.ax.set_title("Crime rates for: {} between {} and {} in {}".format(offense, yr, eyr, state))
        def boom():
            root.destroy()
        button = tk.Button(root, text='Back', width=25, command =lambda: boom())
        button.pack()

