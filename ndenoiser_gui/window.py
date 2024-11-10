import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from datetime import datetime

from .utils import QueuedFile,FileStatus
from .connector import Connector

class NDenoiser_GUI:

    def __init__(self):
        self.queueFiles: dict[str, QueuedFile] = {}
        self.InitGUI()

    def InitGUI(self):
        self.root = tk.Tk()
        self.root.title("Neuroimage Denoiser GUI")
        self.root.geometry("600x600")

        Connector.ImportNDenoiser()

        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        self.menuFile = tk.Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.menuFile)
        self.menuFile.add_command(label="Open File(s)", command=self.MenuFile_OpenFile)

        self.menuDenoiser = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Neuroimage Denoiser", menu=self.menuDenoiser)
        self.menuDenoiser.add_command(label="Test Installation", command=self.MenuDenoiser_TestInstallation)

        self.menuAbout = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="About", menu=self.menuAbout)
        self.menuAbout.add_command(label="Info", command=self.MenuAbout_Info)

        self.frameTools = tk.Frame(self.root)
        self.frameTools.pack(side=tk.TOP)
        self.btnOpenFiles = tk.Button(self.frameTools, text="Open File(s)", command=self.MenuFile_OpenFile)
        self.btnOpenFiles.pack(side=tk.LEFT, padx=20)
        self.btnDenoise = tk.Button(self.frameTools, text="Start Denoising")
        self.btnDenoise.pack(side=tk.LEFT, padx=20)


        self.tvFiles = ttk.Treeview(self.root, columns=("Status"))
        self.tvFiles.heading("#0", text="Path")
        self.tvFiles.heading("Status", text="Status")
        self.tvFiles.column("Status", width=15)
        self.tvFiles.pack(fill="both", expand=True)

        self.txtLog = scrolledtext.ScrolledText(self.root, height=10)
        self.txtLog.configure(state='disabled')
        self.txtLog.pack(side=tk.BOTTOM, fill="x")

        self.Log("Started Neuroimage Denoiser GUI")
        self.UpdateTVFiles()
        self.root.mainloop()

    def Log(self, msg):
        self.txtLog.configure(state='normal')
        self.txtLog.insert(tk.END, f"{datetime.now().strftime('[%x %X]:')}{msg}\n")
        self.txtLog.configure(state='disabled')

    def UpdateTVFiles(self):
        _files = [x for x in self.queueFiles.keys()]
        for qfIndex in self.tvFiles.get_children():
            entryValues = self.tvFiles.item(qfIndex)["values"]
            if not qfIndex in _files:
                self.treeROIs.delete(qfIndex)
                continue
            _files.remove(qfIndex)
            qf = self.queueFiles[qfIndex]
            if entryValues[0] != qf.status.value:
                self.tvFiles.set(qf.id, column="Status", value=qf.status.value)
        for qfIndex in _files:
            qf = self.queueFiles[qfIndex]
            self.tvFiles.insert('', 'end', iid=qf.id, text=qf.path, values=(qf.status.value))
            

    def MenuFile_OpenFile(self):
        files = filedialog.askopenfilenames(parent=self.root, title="Neuroimage Denoiser - Open an file", 
                filetypes=(("All compatible files", "*.tif *.tiff *.stk *.nd2"), 
                           ("TIF File", "*.tif *.tiff *.stk"), 
                           ("ND2 Files (NIS Elements)", "*.nd2"), 
                           ("All files", "*.*")) )
        if files is None or files == "":
            return
        for path in files:
            qf = QueuedFile(path)
            self.queueFiles[qf.id] = qf
        self.UpdateTVFiles()

    def MenuDenoiser_TestInstallation(self):
        nd.help()

    def MenuAbout_Info(self):
        messagebox.showinfo("Neuroimage Denoiser", "Neuroimage Denoiser for removing noise from transient fluorescent signals in functional imaging. Stephan Weissbach, Jonas Milkovits, Michela Borghi, Carolina Amaral, Abderazzaq El Khallouqi, Susanne Gerber, Martin Heine bioRxiv 2024.06.08.598061; doi: https://doi.org/10.1101/2024.06.08.598061\n\nGUI Implementation by Andreas Brilka")