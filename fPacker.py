from posixpath import basename
import tkinter as tk
from customtkinter import *
from tkinter import filedialog as fd
from zipfile import ZipFile
import py7zr
import rarfile
class App(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
        self.main_frame = CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10)
        title = CTkLabel(master=self.main_frame, text="FILE PACKER")
        title.grid(row=0, column=0, pady=(0, 20))
        self.zipSelected=StringVar()
        self.zipSelected.set("off")
        self.zip7Selected=StringVar()
        self.zip7Selected.set("off")
        self.rarSelected=StringVar()
        self.keepStructure=StringVar()
        self.keepStructure.set("off")
        self.selectFormat=CTkLabel(master=self.main_frame,text="SELECT FORMAT")
        self.selectFormat.grid(row=1,sticky="W")
        self.zipCB=CTkCheckBox(master=self.main_frame,text=".Zip",command=self.showFdialogButton,
                               variable=self.zipSelected, onvalue="on", offvalue="off")
        #self.zipCB.grid(row=1,column=0,sticky="W")
        self.zip7CB=CTkCheckBox(master=self.main_frame,text=".7zip",command=self.showFdialogButton,
                                variable=self.zip7Selected, onvalue="on", offvalue="off")
        self.rarCB=CTkCheckBox(master=self.main_frame,text=".RAR",command=self.showFdialogButton,
                               variable=self.rarSelected,onvalue="on",offvalue="off")
     
        self.fdStructure=CTkCheckBox(master=self.main_frame,text="Keep folder struc.",
                                     variable=self.keepStructure, onvalue="on", offvalue="off")
        self.fileDialogBtn=CTkButton(master=self.main_frame,text="Select files", command=self.openFileDialog)
        self.selectedFiles=tk.Listbox(master=self.main_frame,height=10,width=75)
        self.selectedFiles.grid(row=4,column=0)
        self.selectedFiles.bind("<Button-3>",self.removeSelectedItem)
        self.packBtn=CTkButton(master=self.main_frame,text="Pack files",command=self.selectPackType)
        self.packBtn.grid(row=5,column=0,sticky="W",pady=10)
        self.files=[]
        self.packInfo=CTkLabel(master=self.main_frame,text="Info")
        self.packInfo.grid(row=5,column=1)
        self.itemNumber=0
        self.click=0
        menubar=tk.Menu(master=self.master)
        mOption1 = tk.Menu(menubar, tearoff=0)
        mOption1.add_command(label="Pack Files",command=self.showPackingOptions)
        mOption1.add_separator()
        mOption1.add_command(label="Unpack Files")
        self.config(menu=menubar)

        menubar.add_cascade(label="Start",menu=mOption1)
    
    def showPackingOptions(self):
        self.zipCB.grid(row=2,column=0,sticky="W")
        self.zip7CB.grid(row=3,column=0,pady=10,sticky="W")
        #self.rarCB.grid(row=1,column=1,pady=10,sticky="W")
        

    def showFdialogButton(self):
        self.click+=1
        if self.click % 1 == 0:
            self.fileDialogBtn.grid(row=1,column=0,sticky="E")
            self.fdStructure.grid(row=2,column=0,sticky="E")
        if self.click % 2 == 0:
            self.fileDialogBtn.grid_forget()
            self.fdStructure.grid_forget()
    def openFileDialog(self):
        filename = fd.askopenfilename()
        self.files.append(filename)
        #listboxin elementin lisätään antamalla indeksinumero + arvo. indeksi alkaa numerosta 0
        #joka listan ylin rivi.
        self.selectedFiles.insert(self.itemNumber,filename)
        self.selectedFiles.insert(END,"\n")
        self.itemNumber+=1
    
    #selvittää klikatun lista-elementin indeksiarvon
    def removeSelectedItem(self,event):
        self.listIndex=self.selectedFiles.index(tk.ACTIVE)
        self.selectedFiles.delete(self.listIndex)
        self.files.pop(self.listIndex)
    

    def selectPackType(self):
            print(self.zipSelected.get())
            archiveNameDialog = CTkInputDialog(text="Type ZIP archive name:", title="Give a archive name")
            archiveName=archiveNameDialog.get_input()
            if self.zipSelected.get()=="on":
                if archiveName.endswith(".zip") == False:
                    archiveName=archiveName+".zip"  
                    self.packFilesZip(archiveName)
                else:
                    self.packFilesZip(archiveName) 
            elif self.zip7Selected.get()=="on" and archiveName.endswith(".7z") == False:
                archiveName=archiveName+".7z"
                self.pack7zipFiles(archiveName)
            elif self.rarSelected.get()=="on":
                self.packFilesRar(archiveName)
          
    def pack7zipFiles(self,archiveNameFinal):
        # a=append eli liittää, tiedostolistan tiedoston liitetään
        #yksitellen zip-pakettiin.
        with py7zr.SevenZipFile(archiveNameFinal, 'a') as zip7:
            for i in self.files:
                zip7.write(i)
            


    def packFilesZip(self,archiveNameFinal):
        with ZipFile(archiveNameFinal,'w') as zip:
            if self.keepStructure.get()=="off":
                for i in self.files:
                #basename pakkaa tiedostot ilman kansioita
                    zip.write(i,basename(i))
                    #infolist sisältää tietoja kuten paketin koko yms
                    for info in zip.infolist():
                        self.packInfo.configure(text=info.compress_size)
            else:
                 for i in self.files:
                    zip.write(i)
                    #infolist sisältää tietoja kuten paketin koko yms
                    for info in zip.infolist():
                        self.packInfo.configure(text=info.compress_size)

                
    def packFilesRar(self,archivename):
       os.system('rar a',archivename,self.files)


 
 
app = App()
app.geometry("400x240")
app.mainloop()