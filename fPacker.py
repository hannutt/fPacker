import datetime
from datetime import datetime
from posixpath import basename
import tkinter as tk
from customtkinter import *
from tkinter import filedialog as fd
from zipfile import ZipFile
import py7zr
from rarfile import RarFile
from PIL import Image
import pathlib
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
        self.rarSelected.set("off")
        self.keepStructure=StringVar()
        self.keepStructure.set("off")
        self.insertPsw=StringVar()
        self.insertPsw.set("off")
       
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

        self.passwordCB=CTkCheckBox(master=self.main_frame,text="Insert psw",
                                    variable=self.insertPsw, onvalue="on",offvalue="off",command=self.showPswField)
        self.fileDialogBtn=CTkButton(master=self.main_frame,text="Select files", command=self.openFileDialog)

        self.selectedFiles=tk.Listbox(master=self.main_frame,height=10,width=75)
        self.selectedFiles.grid(row=4,column=0)
        self.selectedFiles.bind("<Button-3>",self.removeSelectedItem)
        self.packBtn=CTkButton(master=self.main_frame,text="Pack files",command=self.selectPackType)
        self.packBtn.grid(row=5,column=0,sticky="W",pady=10)
        self.passWordEntry=CTkEntry(master=self.main_frame)
        self.files=[]
        self.packInfo=CTkLabel(master=self.main_frame,text="Info")
        self.packInfo.grid(row=5,column=1)
        self.itemNumber=0
        self.click=0
        menubar=tk.Menu(master=self.master)
        packing = tk.Menu(menubar, tearoff=0)
        packing.add_command(label="Pack Files",command=self.showPackingOptions)
        packing.add_separator()
        packing.add_command(label="Unpack Files")
        self.config(menu=menubar)
        formats=tk.Menu(menubar,tearoff=0)
        formats.add_command(label="Compress image",command=self.imageCompress)


        menubar.add_cascade(label="Start",menu=packing)
        menubar.add_cascade(label="Image compression",menu=formats)
    
    def showPackingOptions(self):
        self.zipCB.grid(row=2,column=0,sticky="W")
        self.zip7CB.grid(row=3,column=0,pady=10,sticky="W")
        self.rarCB.grid(row=3,column=0,pady=10,sticky="E")
       
    def showPswOption(self):
        if self.zip7Selected.get()=="on":
            self.zipCB.grid_forget()
            self.rarCB.grid_forget()
            self.passwordCB.grid(row=2,column=0,sticky="W")
        else:
            self.passwordCB.grid_forget()
            self.showPackingOptions()
    
    def showPswField(self):
        if self.insertPsw.get()=="on":
                self.passWordEntry.grid(row=3,column=0,sticky="E")
        else:
            self.passWordEntry.grid_forget()
        

    def showFdialogButton(self):
        self.click+=1
        if self.click % 1 == 0:
            self.fileDialogBtn.grid(row=1,column=1,sticky="E")
            self.fdStructure.grid(row=2,column=1,sticky="E")
            self.showPswOption()
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
            elif self.zip7Selected.get()=="on":
                if archiveName.endswith(".7z") == False:
                    archiveName=archiveName+".7z"
                    self.pack7zipFiles(archiveName)
                else:
                    self.pack7zipFiles(archiveName)
            elif self.rarSelected.get()=="on":
                self.packFilesRar(archiveName)
         
          
    def pack7zipFiles(self,archiveName):
        if self.insertPsw.get()=="on":
            self.pack7ZipWithPassword(archiveName)
        # a=append eli liittää, tiedostolistan tiedoston liitetään
        #yksitellen zip-pakettiin.
        else:
            with py7zr.SevenZipFile(archiveName, 'a') as zip7:
                for i in self.files:
                    zip7.write(i)

    def pack7ZipWithPassword(self,archiveName):
        self.userInput=self.passWordEntry.get()
        with py7zr.SevenZipFile(archiveName,'a',password=self.userInput) as zip7:
            for i in self.files:
                zip7.write(i)


    def packFilesZip(self,archiveName):
        with ZipFile(archiveName,'w') as zip:
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
        currentDir=os.getcwd()
        with RarFile(currentDir,'w') as rar:
            for i in self.files:
                rar.write(i,arcname=archivename)
    

    def imageCompress(self):
        filename = fd.askopenfilename()
        qualityDialog=CTkInputDialog(text="Type a quality value",title="Quality value")
        qualityValue=qualityDialog.get_input()
        qualityValue=int(qualityValue)
        picture = Image.open(filename)
        now = datetime.now()
        nowStr = now.strftime("%Y%m%d%H%M%S")
        picture.save("Compressed"+nowStr+".jpg", optimize = True, quality = qualityValue)




 
 
app = App()
app.geometry("500x500")
app.mainloop()