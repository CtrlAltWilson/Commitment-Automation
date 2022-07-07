from tkinter import *
from tkinter import ttk
from threading import *
import tkinter

from src.constrants import startGUI,driver, action, addminutes,autorun
from src.config import getConfig, setAutorun
from src.end import end
from src.updatetk import updatetk as status
from src.browser import mainLaunch
from src.tabs import createTab, defaultTabs, closeTab, switchTab
from src.agentcount import agentCount
from src.checkCases import checkCases
from src.setCases import setNewCase
from src.setCommit import setCommit

def preload():
    global driver, action, B2
    B2.grid_forget()
    autoChk.grid_forget()
    driver = mainLaunch(root,config,driver, B1)
    if driver == -1:
        status(B1,"Error starting")
        return
    status(B1,"Creating tabs")
    defaultTabs(driver)
    status(B1,"Getting to work")
    threadworker(0)

def main():
    global addminutes
    ac = agentCount(driver,root,B1)
    if ac > 1:
        addminutes = 2
    else:
        addminutes = 60
    cc = checkCases(driver,B1, root)
    if cc == 0:
        status(B1,"No cases found, sleeping...")
        cleanup(60000,1)
        return
    createTab(driver,cc)
    sc = setNewCase(root,B1,driver)
    if sc == 0:
        status(B1,"Case err, restarting...")
        cleanup(60000,3)
        return
    sco = setCommit(driver,B1,root,addminutes)
    if sco == 0:
        status(B1,"Commit err, restarting...")
        cleanup(60000,3)
        return
    status(B1,"Cleaning up")
    cleanup(2000,3)
    return

def cleanup(seconds, option = 0):
    if option == 1:
        root.after(seconds, main)
    elif option == 3:
        switchTab(driver, 0)
        closeTab(driver, 2)
        root.after(seconds, main)
        
def threadworker(runtarget = 1):
    if runtarget == 1:
        Thread(target=preload).start()
    else:
        Thread(target=main).start()
#Deprecated
def pausebtn():
    status(B2,"Continue",main)
#Deprecated
def contbtn():
    status(B2,"Pause",pausebtn)

def setAutorunMain():
    print("Writing to config") 
    print(autorun.get())

    setAutorun(autorun.get())
    config['autorun'] = autorun.get()
    if autorun.get() == "1":
        countdown(5)

def countdown(count):
    status(B1,str(count))

    if count > 0:
        if autorun.get() == "0":
            status(B1,"Welcome to the commitment automation tool!")
            setAutorunMain()
            return
        # call countdown again after 1000ms (1s)
        root.after(1000, countdown, count-1)
    else:
        if autorun.get() == "1":
            threadworker()
        else:
            return

if startGUI == 0:
    threadworker()
else:
    root = Tk()
    root.title("Commitment Manager")
    root.geometry("250x150")
    root.grid_columnconfigure(0,weight=1)
    frm = ttk.Frame(root, padding=5)
    frm.grid()
    B1 = Label(frm, text="loading...",wraplength=200, justify='center')
    B1.grid(column=0, row=0)

    B2 = ttk.Button(frm, text="Start",command=threadworker)
    B2.grid(column=0,row=1)

    B3 = ttk.Button(frm, text="Quit", command=lambda: end(root,driver))
    B3.grid(column=0, row=2)
    
    config = getConfig(B1)
    autorun = tkinter.StringVar(value=config['autorun'])
    print(autorun)
    status(B1,"Welcome to the commitment automation tool!")
    
    autoChk = (ttk.Checkbutton(root,text="Autorun", variable=autorun,command=setAutorunMain))
    autoChk.grid(column=0,row=3)
    if autorun.get() == "1":
        countdown(5)
    root.mainloop()