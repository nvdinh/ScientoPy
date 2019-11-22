# !/usr/bin/python3
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox

import tkinter.scrolledtext as scrolledtext
from PIL import ImageTk, Image
import globalVar
from PreProcessClass import PreProcessClass
from ScientoPyClass import ScientoPyClass
import webbrowser


class ScientoPyGui:
    def __init__(self):
        self.scientoPy = ScientoPyClass(from_gui=True)

        self.root = Tk()
        self.root.geometry("853x480")
        self.root.title("ScientoPy")

        # Starting the tabs
        nb = ttk.Notebook(self.root)
        preprocess_page = Frame(nb)
        process_page = Frame(nb)

        nb.add(preprocess_page, text='Pre processing')
        nb.add(process_page, text='Analysis')
        nb.pack(expand=1, fill="both")
        nb.select(process_page)

        # Pre processing tab
        img = ImageTk.PhotoImage(Image.open("scientopy_logo.png"))
        logo_panel = Label(preprocess_page, image=img)
        logo_panel.place(relx=0.5, rely=0.4, anchor=CENTER)

        version_label = Label(preprocess_page, text=("Version %s" % globalVar.SCIENTOPY_VERSION))
        version_label.place(relx=0.5, rely=0.7, anchor=CENTER)

        dataset_button = Button(preprocess_page, text="Select dataset", command=self.open_dataset)
        dataset_button.place(relx=0.5, rely=0.9, anchor=CENTER)

        # Analysis tab

        Label(process_page, text="Criterion:", borderwidth=10).grid(sticky=W, column=0, row=0)
        self.comboCriterion = ttk.Combobox(process_page, values=globalVar.validCriterion, width=15)
        self.comboCriterion.current(3)
        self.comboCriterion.grid(column=1, row=0)

        Label(process_page, text="Graph type:", borderwidth=10).grid(sticky=W, column=0, row=1)
        self.comboGraphType = ttk.Combobox(process_page, values=globalVar.validGrapTypes, width=15)
        self.comboGraphType.current(0)
        self.comboGraphType.grid(column=1, row=1)

        Label(process_page, text="Start Year:", borderwidth=10).grid(sticky=W, column=0, row=3)
        self.spinStartYear = Spinbox(process_page, from_=1900, to=2100, bg='white',
                                     textvariable=DoubleVar(value=globalVar.DEFAULT_START_YEAR), width=15)
        self.spinStartYear.grid(column=1, row=3)

        Label(process_page, text="End Year:", borderwidth=10).grid(sticky=W, column=0, row=4)
        self.spinEndYear = Spinbox(process_page, from_=1900, to=2100, bg='white',
                                   textvariable=DoubleVar(value=globalVar.DEFAULT_END_YEAR), width=15)
        self.spinEndYear.grid(column=1, row=4)

        Label(process_page, text="Topics length:", borderwidth=10).grid(sticky=W, column=0, row=5)
        self.spinTopicsLength = Spinbox(process_page, from_=0, to=1000, bg='white', textvariable=DoubleVar(value=10),
                                        width=15)
        self.spinTopicsLength.grid(column=1, row=5)

        Label(process_page, text="Window (years):", borderwidth=10).grid(sticky=W, column=0, row=6)
        self.spinWindowWidth = Spinbox(process_page, from_=0, to=100, bg='white', textvariable=DoubleVar(value=2),
                                       width=15)
        self.spinWindowWidth.grid(column=1, row=6)

        process_page.grid_columnconfigure(2, pad=50)

        Label(process_page, text="Custom topics:", borderwidth=10).grid(sticky=W, column=2, row=0, padx=15)
        self.entryCustomTopics = scrolledtext.ScrolledText(process_page, undo=True, bg='white', width=70, height=10)
        self.entryCustomTopics.grid(column=2, row=1, rowspan=5)

        self.chkValuePreviusResults = BooleanVar()
        self.chkValuePreviusResults.set(False)
        checkPreviousResults = Checkbutton(process_page, var=self.chkValuePreviusResults,
                                           text="Use previous results").grid(column=2, row=6, sticky=W, padx=15)

        run_button = Button(process_page, text="Run", command=self.scientoPyRun)
        run_button.grid(column=0, row=7, sticky=W)

        results_button = Button(process_page, text="Open results table", command=self.open_results)
        results_button.grid(column=1, row=7, sticky=W)

        ext_results_button = Button(process_page, text="Open extended results", command=self.open_ext_results)
        ext_results_button.grid(column=2, row=7, sticky=W)

    def open_results(self):
        webbrowser.open(self.scientoPy.resultsFileName)

    def open_ext_results(self):
        print(self.scientoPy.extResultsFileName)
        webbrowser.open(self.scientoPy.extResultsFileName)

    def scientoPyRun(self):
        print(self.chkValuePreviusResults.get())

        self.scientoPy.closePlot()

        self.scientoPy.criterion = self.comboCriterion.get()
        self.scientoPy.graphType = self.comboGraphType.get()
        self.scientoPy.startYear = int(self.spinStartYear.get())
        self.scientoPy.endYear = int(self.spinEndYear.get())
        self.scientoPy.length = int(self.spinTopicsLength.get())
        self.scientoPy.windowWidth = int(self.spinWindowWidth.get())
        self.scientoPy.previousResults = self.chkValuePreviusResults.get()

        if bool(self.entryCustomTopics.get("1.0", END).strip()):
            self.scientoPy.topics = self.entryCustomTopics.get("1.0", END).replace("\n",";")
        else:
            self.scientoPy.topics = ''

        self.scientoPy.scientoPy()


    def open_dataset(self):
        self.root.dir_name = filedialog.askdirectory()
        if not self.root.dir_name:
            return

        preprocess = PreProcessClass(from_gui=True)
        preprocess.dataInFolder = self.root.dir_name
        totalPapers = preprocess.preprocess()
        if totalPapers == 0:
            messagebox.showinfo("Error", "No valid dataset files found in: %s" % self.root.dir_name)


    def runGui(self):
        self.root.mainloop()


if __name__ == '__main__':
    scientoPyGui = ScientoPyGui()
    scientoPyGui.runGui()