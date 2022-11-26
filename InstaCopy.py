import os,shutil
from configparser import ConfigParser
from datetime import datetime
import tkinter as tk
from tkinter import DISABLED, NORMAL, END, filedialog, font, RIGHT, Y, BOTH, VERTICAL, LEFT
from PIL import Image, ImageTk
from functools import partial

config_object=ConfigParser()

###########################################################################
version=("1.3.0")
###########################################################################
def changeLog():
    global root
    root = tk.Tk()
    root.geometry("800x400")
    root.resizable(0,0)
    canvas = tk.Canvas(root, borderwidth=0)
    frame = tk.Frame(canvas)
    vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)

    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((4,4), window=frame, anchor="nw")

    frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

    populate(frame)

    root.mainloop()

def createLogList():
    global logList
    
    logList=[]
    logList.append("1.3.0 (3/29/20) Refresh button & Scrollbar added to main menu. Scrollbar added to GUI that appears when files are copied.")
    logList.append("1.2.9 (3/25/20) Scrollbar added to Change Log.")
    logList.append("1.2.8 (3/23/20): CR2 thumbnails are shown as a blank CR2 file icon.")
    logList.append("1.2.7 (3/22/20): Removed Help menu, rearranged main menu a little bit.")
    logList.append("1.2.6 (3/21/20): Added individual tabs in settings. Prefix utility changed to Replace ____ with _____ feature.")
    logList.append("1.2.5 (3/20/20): Function to individually select photos added. Photo caption appears red if photo has been copied before.")
    logList.append("1.2.4 (3/19/20): Frame of photo button turns green if selected. Main menu no longer resizable.\nSelect New button added, which selects all files that haven't been copied before.")
    logList.append("1.2.3 (3/6/20): Main Menu layout reorganized once again. Select All checkbox added to make copying all files easier.")
    logList.append("1.2.2 (3/2/20): Program now creates 'InstaCopyFiles.txt', a file that contains names of all the files that get copied.\n Only files that have not been copied yet will be copied.")
    logList.append("1.2.1 (2/24/20): Reworked the main menu to include all photos in the file.")
    logList.append("1.2.0 (2/22/20): Minimum Viable Product now available as .exe")
    logList.append("1.1.8 (2/21/20): Fixed folder & prefix errors when loading program for the first time. Changed several font/sizes of text, added Help button,\nand removed Bugs & Errors button.")
    logList.append("1.1.7 (2/20/20): Fixed prefix textbox issues. Changed font of Main Menu titles. \nFixed bugs that occur when user starts program and immediately copies files.")
    logList.append("1.1.6 (2/19/20): Prefix & Folder checkboxes now save.")
    logList.append("1.1.5 (2/16/20): Fixed incorrect pop-up when loading program for the first time. Logging & prefix system fixed.")
    logList.append("1.1.4 (2/15/20): Browse Files button added to both directories, User no longer needs to manually enter folder paths.\nPrefix not saving bug fixed. Changed color of Copy Files button.")
    logList.append("1.1.3 (2/14/20): Added logging system (not fully functional), and known bugs & errors button/screen in Change Log.")
    logList.append("1.1.2 (2/13/20): Fixed bug issues regarding copy errors. Added version text in main menu.")
    logList.append("1.1.1 (2/12/20): Added options for sort-by-folder and prefix. Imports prefix if previously saved.")
    logList.append("1.1.0 (2/12/20): Added GUI for copying programs(and appropriate error prompt). Copying mechanism added.")
    logList.append("1.0.9 (2/12/20): Added quit button and title text.")
    logList.append("1.0.5 (2/12/20): Prompt for directories now saves input. Doesn't let user exit settings if directories are incorrect.")
    logList.append("1.0.3 (2/10/20): Change Log user-interface added")
    logList.append("1.0.2 (2/9/20): Main menu added & Settings button added. Settings currently has prompts for both directories.")
    logList.append("1.0.0 (2/9/20): Fully functioning back-end released. Added change log.")

def populate(frame):
    createLogList()
    
    vText=tk.Label(frame,text=("Current version: "+str(version)),font=("Arial",15))
    vTextFont=font.Font(vText, vText.cget("font"))
    vTextFont.config(underline=True)
    vText.config(font=vTextFont)
    vText.grid(row=0,column=0)
    
    row=1
    for element in logList:
        tk.Label(frame, text=element).grid(row=row, column=0)
        row+=1
    tk.Button(frame,command=root.destroy,text="Return").grid(row=row,column=0)

def onFrameConfigure(canvas): #Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))
###########################################################################
def findSource(): #Opens file browser for source directory
    global sourceDirectory,sourceEntry
    sourceDirectory=filedialog.askdirectory()
    sourceEntry.delete(0,END)
    sourceEntry.insert(0,sourceDirectory)
    #print (sourceDirectory)
###########################################################################
def findRoot(): #Opens file browser for root directory
    global rootDirectory,rootEntry
    rootDirectory=filedialog.askdirectory()
    rootEntry.delete(0,END)
    rootEntry.insert(0,rootDirectory)
    #print (rootDirectory)
###########################################################################
def directoryCheck (): #Validates directories if manually entered 
    global sourceDirectory, rootDirectory

    sourceDirectory=sourceEntry.get() #Checks if directories exist by reading entryboxes(error only possible if user enters manually)
    rootDirectory=rootEntry.get()

    if not os.path.isdir(sourceDirectory) or not (os.path.isdir(rootDirectory)): #Disables save/exit button if directory does not exist
        error=tk.Tk()
        error.title("Error")
        error.geometry ("300x100")
        tk.Label(error,text="1 or more of the directories do not exist. Please try again").pack()
        tk.Button(error,text="Confirm",command=error.destroy).pack()
    
        error.mainloop()
    else: #Enables save/exit button if directory does exist
        setConfig(sourceDirectory,rootDirectory)
###########################################################################
def settings(): #Displays all settings
    global exitButton,setInfoGUI, prefixFolderCanvas, directoryCanvas

    photoMenu.destroy()

    setInfoGUI=tk.Tk() #Main window
    setInfoGUI.title("Image Copy")
    setInfoGUI.geometry("400x100")

    setInfoGUI.resizable(0,0)

    importSettings()

    buttonCanvas=tk.Canvas(setInfoGUI,width=400,height=30)
    buttonCanvas.pack()

    directoryTab()

    directoryCanvasButton=tk.Button(buttonCanvas,text="Directories",command=directoryTab).place(x=10,y=0)
    prefixFolderCanvasButton=tk.Button(buttonCanvas,text="Prefix & Folder",command=PrefixFolderTab).place(x=80,y=0)

    exitButton=tk.Button(setInfoGUI,text="Save & Exit",command=exitSettings,fg="green").place(x=275,y=0) #Saves directories and returns to Main Menu
    tk.Button(setInfoGUI,text="Cancel",command=settingsCancel,fg="red").place(x=350,y=0) #Cancels without saving

    setInfoGUI.mainloop()
###########################################################################
def directoryTab():
    global directoryCanvas, sourceDirectory, rootDirectory,sourceEntry, rootEntry, prefixFolderCanvas
    try:
        prefixFolderCanvas.destroy()
    except Exception as e:
        #print (e)
        pass
    
    directoryCanvas=tk.Canvas(setInfoGUI,width=400,height=70)
    directoryCanvas.pack()
    
    tk.Label(directoryCanvas,text="Source Directory:").place(x=6,y=0)
    tk.Label(directoryCanvas,text="Root Directory:").place(x=6,y=30)

    tk.Button(directoryCanvas,text="Browse",command=findSource).place(x=350,y=0)
    tk.Button(directoryCanvas,text="Browse",command=findRoot).place(x=350,y=30)

    sourceEntry=tk.Entry(directoryCanvas,exportselection=0,width=40)
    sourceEntry.place(x=100,y=0)

    rootEntry=tk.Entry(directoryCanvas,exportselection=0,width=40)
    rootEntry.place(x=100,y=30)
    
    try: #Trys to fill in directory entryboxes if .ini contains info
        sourceEntry.insert(0,sourceDirectory)
        rootEntry.insert(0,rootDirectory)
    except:
        pass
###########################################################################
def PrefixFolderTab():
    global prefixEntry, prefixVal, folderVal, folderCheckBox, prefixFolderCanvas, replaceEntry
    
    prefixFolderCanvas=tk.Canvas(setInfoGUI,width=400,height=170)
    prefixFolderCanvas.place(x=0,y=30)
    
    prefixVal=tk.BooleanVar()
    folderVal=tk.BooleanVar()
    importSettings() #To autocheck boxes & autofill blanks
    
    PrefixCheckBox=tk.Checkbutton(prefixFolderCanvas,text="Enable Prefix",command=prefixCommand,var=prefixVal).place(x=10,y=0)
    
    tk.Label(prefixFolderCanvas,text="Replace").place(x=10,y=30)
    tk.Label(prefixFolderCanvas,text="with").place(x=190,y=30)
    
    replaceEntry=tk.Entry(prefixFolderCanvas,exportselection=0,state=DISABLED)
    replaceEntry.place(x=60,y=30)

    prefixEntry=tk.Entry(prefixFolderCanvas,exportselection=0,state=DISABLED)
    prefixEntry.place(x=225,y=30)

    folderCheckBox=tk.Checkbutton(prefixFolderCanvas,text="Organize folders by Date",command=folder, var=folderVal).place(x=170,y=0)
    
    try: #Trys to check checkboxes if .ini contains info
        importPrefix()
        if prefixBox=="True":
            prefixEntry.config(state=NORMAL)
            prefixEntry.insert(0,prefix)
            replaceEntry.config(state=NORMAL)
            replaceEntry.insert(0,replaceString)
    except Exception as e:
        print ("prefixFolderTab",e)
        pass
###########################################################################
def settingsCancel():
    setInfoGUI.destroy()
    mainMenu()
###########################################################################
def folder(): #Runs if user wants to sort into folders
    global promptFolder,folderCheckBox

    if promptFolder==False: #Folder checkbox is checked
        promptFolder=True

    else: #Folder checkbox is unchecked
        promptFolder=False

###########################################################################
def importAll(): #Only used when program is opened
    global prefixBox,folderBox,sourceDirectory,rootDirectory, prefix, promptFolder, replaceString
    try:
        config_object.read("InstaCopySettings.ini") #Reads .ini   
        try:
            boxSettings=config_object["CheckBox Settings"] #Reads preset prefix and folder checkbox status
            prefixBox=boxSettings["prefixBox"]
            folderBox=boxSettings["folderBox"]
            if prefixBox=="True": #If prefix checkbox was checked, reads previous prefix
                #print ("in if")
                prefixInfo=config_object["prefixInfo"]
                prefix=prefixInfo["prefix"]
                replaceString=prefixInfo["replace"]
            if folderBox=="True": #Used to autofill checkbox in Settings
                promptFolder=True
            else:
                promptFolder=False
        except:
            promptFolder=False
            #print("promptFolder1=",promptFolder)
        try:
            userinfo=config_object["userinfo"] #Trys to read previous directories
            sourceDirectory=userinfo["sourceDirectory"]
            rootDirectory=userinfo["rootDirectory"]
        except: #No previously used directories
            pass
    except Exception as e:
        print ("ERROR1...",e)
      #  print ("promptFolder2=",promptFolder)
###########################################################################
def prefixCommand(): #Enables/disables and inserts saved prefix to text box
    global prefix, prefixEntry, prefixBox, replaceEntry
    try:
        if prefixBox=="False": #Prefix checkbox is already unchecked
            importPrefix() #Imports saved prefix
            prefixEntry.config(state=NORMAL) #Enables entry field
            replaceEntry.config(state=NORMAL)
            prefixBox=("True")
            try:
                prefixEntry.insert(0,prefix) #Fills in existing prefix (if exists)
                replaceEntry.insert(0,replaceString)
            except:
                pass 
        else: #Prefix checkbox is already checked
            prefixBox=("False")
            prefixEntry.delete(0,END)
            prefixEntry.config(state=DISABLED)
            replaceEntry.delete(0,END)
            replaceEntry.config(state=DISABLED)
    except Exception as e:
       # print (e)
        prefixEntry.config(state=NORMAL)
        replaceEntry.config(state=NORMAL)
        prefixBox=("True")
###########################################################################
def exitSettings(): #Runs if user clicks 'Save & Exit' button in Settings
    global prefix, sourceDirectory,rootDirectory,replaceString
    directoryCheck() #Makes sure directories exists

    sourceDirectory=sourceEntry.get()
    rootDirectory=rootEntry.get()
    
    setConfig(sourceDirectory,rootDirectory) #Saves current directories to .ini
    
    try:
        checkSettings(prefixVal.get(),folderVal.get()) #Saves current state of checkboxes to .ini
        if len(prefixEntry.get())!=0 or len(replaceEntry.get()): #If user has entered something into prefix or entrybox, updates it in .ini
            setPrefix()
            prefix=prefixEntry.get()
            replaceString=replaceEntry.get()
    except Exception as e:
        print ("exitSettings",e)
    
    setInfoGUI.destroy()
    mainMenu()
###########################################################################
def checkSettings(prefixVal,folderVal): #Reapplies checkboxes(prefix & folder) settings
    try: #Read in order to see if checkboxes should be checked or not
        config_object["CheckBox Settings"]={
            "prefixBox":prefixVal,
            "folderBox":folderVal
        }
        with open("InstaCopySettings.ini","w") as conf:
            config_object.write(conf)
    except:
        pass
###########################################################################
def importSettings(): #Imports previous settings for both checkboxes
    global prefixVal, folderVal, prefixBox, folderBox
    try:
        config_object.read("InstaCopySettings.ini") 
        boxSettings=config_object["CheckBox Settings"]
        prefixBox=boxSettings["prefixBox"]
        folderBox=boxSettings["folderBox"]
      #  print (prefixBox)
      #  print (folderBox)
        
        if prefixBox=="True": #Checks prefix box
            prefixVal.set(True)
        else:
            prefixVal.set(False)
        if folderBox=="True": #Checks folder box
            folderVal.set(True)
        else:
            folderVal.set(False)
    except:
        pass
   #print (prefixBox)
   # print (folderBox)
###########################################################################
def setConfig(source,root): #Updates/sets source/root directories to .ini
    config_object["userinfo"]={
        "sourceDirectory": source,
        "rootDirectory": root
    }
    with open("InstaCopySettings.ini","w") as conf: #Write above lines to InstaCopySettings.ini file
        config_object.write(conf)
        
###########################################################################
def setPrefix(): #Updates prefix to .ini
    global prefix,replaceString
    prefix=prefixEntry.get()
    replaceString=replaceEntry.get()
    config_object["prefixInfo"]={
        "prefix": prefix,
        "replace": replaceString
    }
    with open("InstaCopySettings.ini","w") as conf: #Write above lines to InstaCopySettings.ini file
        config_object.write(conf)
        
###########################################################################
def importConfig(): #Imports previously saved directories
    global sourceDirectory,rootDirectory
    try:
        config_object.read("InstaCopySettings.ini") #Read InstaCopySettings.ini file
        userinfo=config_object["userinfo"]
        sourceDirectory=userinfo["sourceDirectory"]
        rootDirectory=userinfo["rootDirectory"]
    except:
        print ("No saved data")
        error=tk.Tk()
        error.title("Error")
        error.geometry ("300x100")
        tk.Label(error,text="No saved data to import").pack()
        tk.Button(error,text="Confirm",command=error.destroy).pack()
    
        error.mainloop()
###########################################################################
def importPrefix(): #Imports prefix from .ini
    global prefix,replaceString
    try:
        config_object.read("InstaCopySettings.ini")
        prefixInfo=config_object["prefixInfo"]
        prefix=prefixInfo["prefix"]
        replaceString=prefixInfo["replace"]
    except Exception as e:
        print("importPrefix",e)
###########################################################################
def copyBackEnd(): #Performs all List duties necessary to copy fles
    global sourceDirectory,rootDirectory, pathList, sourceList
    sourceList=[] #List with all files within sourceDirectory
    copiedList=[]
    if not (os.path.isdir(sourceDirectory)) or not (os.path.isdir(rootDirectory)): #If directories selected dont exist, displays error
        error=tk.Tk()
        error.title("Error")
        error.geometry ("300x100")
        tk.Label(error,text="Current selected directories do not exist").pack()
        tk.Button(error,text="Confirm",command=error.destroy).pack()
    
        error.mainloop()
    else: #Source/Root directories exist
        #print ("True")
        for entry in os.listdir(sourceDirectory): #Adds all file names to sourceList
            sourceList.append(entry)
       # print (sourceList)
        pathList=[]

        for element in sourceList: #Adds all file paths to pathList
            path=(str(sourceDirectory)+"/"+str(element))
            pathList.append(path)
        #print (pathList)
        if len(sourceList)==0: #If no files within the sourceDirectory, reroutes to reenter source
            error=tk.Tk()
            error.title("Error")
            error.geometry ("300x100")
            tk.Label(error,text="No files in source directory").pack()
            tk.Button(error,text="Confirm",command=error.destroy).pack()
            sourceList=[]
            pathList=[]

    
            error.mainloop()
###########################################################################
def fileCopy(): #Copies files
    global skipped,fileNum, prefix, log, error, copyGUI
    log=open("InstaCopyLog.txt","a")
    fileList=open("InstaCopyFiles.txt","a")
    
    checkSelection()
    if valError==True:
        return

    importConfig()
  #  copyBackEnd()
    
    fileNum=0
    skipped=0
    
    try:
        if "prefix" in locals() or "prefix" in globals():
            #print (prefixBox)
            if prefixBox=="True":
                print ("Prefix=",prefix)
            else:
               # print ("In try-if-if, no prefix")
                prefix=""
        else:
          #  print ("In try, no prefix")
            prefix=""
    except:
      #  print ("No prefix")
        prefix=""
    
    copyGUI=tk.Tk()
    copyGUI.geometry("350x300")
    canvas=tk.Canvas(copyGUI,borderwidth=0)
    frame=tk.Frame(canvas)
    vsb=tk.Scrollbar(canvas,orient="vertical",command=canvas.yview)
    canvas.config(yscrollcommand=vsb.set)

    vsb.pack(side="right",fill="y")
    canvas.pack(side="left",fill="both",expand=True)
    canvas.create_window((4,4),window=frame,anchor="nw")

    frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

    row=0

    for file in toCopyList: #Copies every file within sourceDirectory
        fileNum+=1
        tk.Label(frame,text=("Copying",file,"(File",fileNum,"of",str(len(toCopyList))+")")).grid(row=row,column=0)
        element=file.replace(str(sourceDirectory)+"/","")

        row+=1

        try:
            if len(replaceString)==0:
                element=str(prefix)+element
            elif replaceString in element:
                element=element.replace(replaceString,prefix)
        except:
            pass
        try:
            time=datetime.now()
            time=str(time)
            if promptFolder==True: #Runs if user wants to create date folders
                imageDateList=[]
                imageDate=os.stat(file).st_ctime
                imageDate=datetime.fromtimestamp(imageDate)
                imageDate=str(imageDate)
                imageDate=imageDate[:10]
                imageDateList.append(imageDate) #Image date
                for entry in imageDateList:
                    folderPath=(rootDirectory+"/"+entry)    
                    if not os.path.exists(folderPath): #Creaters folder if doesn't already exist
                        os.makedirs(folderPath)
                    shutil.copy2(file,folderPath+"//"+str(element)) #Copies file
                    log.write(str(file)+" copied to "+str(folderPath)+"//"+str(element)+"\nTime: "+str(time)+"\nPlaced into folder "+str(imageDate)+"\n\n")

            else: #User doesn't want to sort by folders
                shutil.copy2(file,str(rootDirectory)+"//"+str(element)) #Copies file
                log.write(str(file)+" copied to "+str(rootDirectory)+"//"+str(element)+"\nTime: "+str(time)+"\n\n")

            fileList.write(str(file)+"\n")
        except Exception as e: #If error, prompts user whether they want to skip file or retry
            print ("ERROR:",e)
            copyGUI.destroy()
            error=tk.Tk()
            error.title="Error"

            tk.Label(error,text=("Error while copying"+str(file))).pack()
            tk.Button(error,text="Retry",command=retry).pack()
            tk.Button(error,text="Skip",command=skip).pack()
            try:
                if promptFolder==True: #Prints to log
                    log.write("ERROR: "+str(e)+"\n"+str(file)+" attempted to copy to"+(folderPath)+"//"+prefix+str(element)+"\nTime: "+str(time)+"\nPlaced into folder "+str(imageDate)+"\n\n")
                    print ("ERROR: "+str(e)+"\n"+(file)+" attempted to copy to"+(folderPath)+"//"+prefix+str(element)+"\nTime: "+str(time)+"\nPlaced into folder "+str(imageDate)+"\n\n")
            except:
                log.write("ERROR :"+str(e)+"\n"+str(file)+" attempted to copy to "+str(rootDirectory)+"//"+prefix+str(element)+"\nTime: "+time+"\n\n")
                print ("ERROR :"+str(e)+"\n"+str(file)+" attempted to copy to "+str(rootDirectory)+"//"+prefix+str(element)+"\nTime: "+time+"\n\n")

            error.mainloop()
    
    copyComplete=tk.Label(frame,text=("\nCopy Complete\nFiles copied:"+str(fileNum)+"\nFiles skipped:"+str(skipped)),fg="green",font=(10)).grid(row=row,column=0)
    row+=1
    tk.Button(frame,text="Return to Main Menu",command=copyFinished).grid(row=row,column=0)
    
    log.close()
    fileList.close()
    copyGUI.mainloop()
###########################################################################
def copyFinished(): #Returns to main menu after user selects button after copying finishes
    copyGUI.destroy()
    refresh()
###########################################################################
def retry(): #If error during copying and User clicks retry
    error.destroy()
    fileCopy()
###########################################################################
def skip(): #If error during copying and User clicks Skip File
    global skipped,fileNum
    error.destroy()
    skipped+=1
    fileNum-=1
    return
###########################################################################
def createGrid(GUI): #Sets up a 20 by 20 grid for GUIs sent through this
    rows=0
    while rows<20:
        GUI.rowconfigure(rows,weight=1)
        GUI.columnconfigure(rows,weight=1)
        rows+=1
###########################################################################
def checkSelection(): #Checks to make sure both Select New & Select All are not selected
    global error,valError
    if newVal.get()==True and selectVal.get()==True:
        valError=True
        error=tk.Tk()
        error.title("Error")
        tk.Label(error,text="Cannot select both Select New & Select All at the same time",fg="red").pack()
        tk.Button(error,text="Return",command=error.destroy).pack()
        error.mainloop()
    else:
        valError=False
###########################################################################
def mainMenu(): #Main menu
    global photoMenu, toCopyList, photoButton, sourceList, selectVal, selectAllCheckBox, propertiesList, index, photoList, photo, newVal, objectList
    photoMenu=tk.Tk()
    photoMenu.title("Insta-Copy")
    photoMenu.geometry("1720x1080")
    photoMenu.resizable(0,0)
    
    buttonCanvas=tk.Canvas(photoMenu,width=1720,height=180)
    buttonCanvas.pack()
    
   # fullscreenCanvas=tk.Canvas(photoMenu,width=600,height=1080)
   # fullscreenCanvas.pack()

  #  tk.Label(fullscreenCanvas,text="test").pack()

    photoCanvas=tk.Canvas(photoMenu,borderwidth=0)
    frame=tk.Frame(photoCanvas)
    vsb=tk.Scrollbar(photoMenu,orient="vertical",command=photoCanvas.yview)
    photoCanvas.config(yscrollcommand=vsb.set)

    vsb.pack(side="right",fill="y")
    photoCanvas.pack(side="left",fill="both",expand=True)
    photoCanvas.create_window((4,4),window=frame,anchor="nw")
    createGrid(frame)

    frame.bind("<Configure>", lambda event, canvas=photoCanvas: onFrameConfigure(photoCanvas))

    '''Top Buttons/Labels'''
    tk.Label(buttonCanvas,text="Insta-Copy",font=("Pristina",75)).place(x=50,y=0)
    tk.Label(buttonCanvas,text="Created by Anton Gurevich",font=("Pristina",15)).place(x=75,y=100)
    tk.Button(buttonCanvas,text="Copy Files",command=fileCopy,fg="green",font=("Arial",20)).place(x=800,y=50)
    tk.Button(buttonCanvas,text="Settings",command=settings,font=("Arial",20)).place(x=1150,y=50)
    tk.Button(buttonCanvas,text="Quit",command=photoMenu.destroy,fg="red",font=("Arial",20)).place(x=1450,y=50)
    tk.Button(buttonCanvas,text=("Change Log\n(v. "+str(version)+")"),command=changeLog,font=("Arial",15)).place(x=1300,y=45)
    tk.Label(buttonCanvas,text="*Red text=Already copied*",fg="red",font=("Arial",10,"bold")).place(x=30,y=150)
    tk.Button(buttonCanvas,text="Refresh",command=refresh,font=("Arial",15)).place(x=830,y=5)

    try: #Checks if .ini exists
        copyBackEnd()
        tk.Label(buttonCanvas,text="Select Files to Copy",font=("Arial",25)).place(x=450,y=50)
    except: #Only runs if program is being run for the first time (or .ini is deleted)
        tk.Label(buttonCanvas,text="To begin,\nselect directories in Settings",font=("Arial",20, "underline")).place(x=450,y=50)
    try: #Checks if file with all previously copied fileNames exists
        fileList=open("InstaCopyFiles.txt","r")
    except:
        pass
    
    x=-100
    y=50
    y2=165
    objectList=[]
    index=-1
    photoList=[]

    row=0
    column=0
    row2=1
    try: #Displays all photos as buttons
        for file in pathList:
            index+=1
            x+=150
            
            fileName=file.replace(sourceDirectory+"/","")
            oldFile = False
            try:
                with open ("InstaCopyFiles.txt") as fileList:
                    if file in fileList.read(): #File has already been copied before
                        tk.Label(frame,text=fileName,fg="red").grid(row=row2,column=column,padx=20)
                        oldFile = True
                    else:
                        tk.Label(frame,text=fileName).grid(row=row2,column=column,padx=20)
            except:
                tk.Label(frame,text=fileName).grid(row=row2,column=column,padx=20)
            if file[-3:]=="CR2" or oldFile:
                #print (True)
                path=os.getcwd()
                blankFile=path+"\BlankFile.png"
                image=Image.open(blankFile)
            else:
                #print (False)
                image=Image.open(file)
            
            image=image.resize((100,100),Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)

            photoButton=tk.Button(frame,image=photo,command=partial(photoSelected,file),borderwidth=5)
            photoButton.image=photo    
            photoButton.grid(row=row,column=column,padx=20)
            
            column+=1

            objectList.append(photoButton)
            photoList.append(file)

            if column==11:
                column=0
                row+=2
                row2+=2

    except Exception as e: #Doesn't run if Settings file doesnt exist
        print (e)
        pass
        
    
    selectVal=tk.BooleanVar()
    selectAllCheckBox=tk.Checkbutton(buttonCanvas,text="Select All",command=copyAll,var=selectVal,font=("Arial",15)).place(x=975,y=50)
    
    newVal=tk.BooleanVar()
    selectNewCheckBox=tk.Checkbutton(buttonCanvas,text="Select New",command=copyNew,var=newVal,font=("Arial",15)).place(x=975,y=80)
    
    propertiesList=[] #[[path,index,toCopy,alreadyCopied][photoButtonObject],[...]]
    index=-1 #Index of all files
    for element in photoList: #Adds all photos to List of Lists
        #print ("element=",element)
        index+=1
        try:
            with open ("InstaCopyFiles.txt") as fileList:
                if element in fileList.read(): #File has already been copied before
                    #print (element,"removed")
                    alreadyCopied=True
                    sourceList.remove(element.replace(sourceDirectory+"/",""))

                else: #File has not been copied before
                    #print (element,"not removed")
                    alreadyCopied=False
        except Exception as e: #Only runs if program is run for the first time
            #print (e)
            alreadyCopied=False 
        toCopy=False
        propertiesList.append([element,index,toCopy,alreadyCopied,photoList[index]])

    index=-1 #Which photo is being referenced
    toCopyList=[]
    for element in propertiesList:
        index+=1
        if propertiesList[index][2]==True and propertiesList[index][3]==False: #Only adds to toCopyList if file hasn't been copied before and file has been selected
            #print ("if True",element)
            toCopyList.append(propertiesList[index][0])
    #print ("propertiesList=",propertiesList)
    #print ("toCopyList=",toCopyList)
    
    photoMenu.mainloop()
###########################################################################
def refresh():
    photoMenu.destroy()
    mainMenu()
###########################################################################
def copyNew():
    global toCopyList
    index=-1
    if newVal.get()==True:
        for element in propertiesList:
            index+=1
            if propertiesList[index][3]==False: #Only adds to toCopyList if file hasn't been copied before
                toCopyList.append(propertiesList[index][0])
                objectList[index].config(background="green")
    else:
        for x in objectList:
            x.config(background="white")
    #print (toCopyList)
###########################################################################
def copyAll(): #Copies all files
    global toCopyList
    if selectVal.get()==True: #Selects all photos
        toCopyList=pathList
        for x in objectList:
            x.config(background="green")
    else:
        for x in objectList: #Unselects all photos
            x.config(background="white")
            toCopyList=[]
###########################################################################        
def photoSelected(file): #Runs if photo is selected in main menu
    global toCopyList
    
    index=photoList.index(file)
    index=objectList[index]
    
    if index.cget("background")=="green": #If photo was already selected, unselects it
        #print (True)
        index.config(background="white")
    else: #If photo was unselected, selects it
        toCopyList.append(file)
        #print (False)
        index.config(background="green")
        #print ("toCopyList=",toCopyList)

###########################################################################
'''Main Program'''
importAll()
mainMenu()
