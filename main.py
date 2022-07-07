from tkinter import *
from tkinter import ttk
from threading import *

from src.constrants import startGUI,driver, action, addminutes,autorun
from src.config import getConfig
from src.end import end
from src.updatetk import updatetk as status
from src.browser import mainLaunch
from src.tabs import createTab, defaultTabs, closeTab, switchTab
from src.agentcount import agentCount
from src.checkCases import checkCases
from src.setCases import setNewCase
from src.setCommit import setCommit

def preload():
    global config, driver, action, B2
    B2.grid_forget()
    config = getConfig(B1)
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
    if ac > 2:
        addminutes = 5
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

if startGUI == 0:
    main()
else:
    root = Tk()
    root.title("Commitment Manager")
    root.geometry("250x100")
    root.grid_columnconfigure(0,weight=1)
    frm = ttk.Frame(root, padding=5)
    frm.grid()
    B1 = Label(frm, text="loading...",wraplength=200, justify='center')
    B1.grid(column=0, row=0)
    status(B1,"Welcome to the commitment automation tool!")
    B2 = ttk.Button(frm, text="Start",command=threadworker)
    B2.grid(column=0,row=1)

    B3 = ttk.Button(frm, text="Quit", command=lambda: end(root,driver))
    B3.grid(column=0, row=2)
    if autorun == 1:
        threadworker()
    root.mainloop()