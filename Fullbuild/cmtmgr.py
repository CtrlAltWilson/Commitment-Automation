from tkinter import *
from tkinter import ttk

from threading import *
import tkinter

from end import end
from browser import mainLaunch
from setCommit import setCommit
from setCases import setNewCase
from agentcount import agentCount
from checkCases import checkCases
from updatetk import updatetk as status
from config import getConfig, setAutorun
from tabs import createTab, defaultTabs, closeTab, switchTab
from constrants import startGUI,driver, action, addminutes,autorun, isStopped, retrymax, finished, bgc, bgaccent, fgc,debug


def preload(preStage = 0):
    global driver, action, B2, finished
    if isStopped == 1: 
        return 
    #B2.grid_forget()
    elif preStage == 0:
        status(B1,"Launching browser")
        autoChk.grid_forget()
        driver = mainLaunch(root,config,driver, B1)
        if driver == -1:
            status(B1,"Error starting")
            return 
    elif preStage == 1:
        status(B1,"Creating tabs")
        defaultTabs(driver)
    elif preStage == 2:
        status(B1,"Getting to work")
        finished = True
        return 
    preload(preStage + 1)

def main(mainStage = 0):
    global addminutes
    while finished == False:
        pass
    if isStopped == 1:
        return
    elif mainStage == 0:
        ac = agentCount(driver,root,B1)
        if ac >= 1:
            addminutes = 2
        else:
            addminutes = 60
    elif mainStage == 1:
        cc = checkCases(driver,B1, root)
        if cc == 0:
            status(B1,"No cases found, sleeping...")
            cleanup(60000,1)
            return
        createTab(driver,cc)
    elif mainStage == 2:
        sc = setNewCase(root,B1,driver)
        if sc == 0:
            status(B1,"Case err, restarting...")
            cleanup(60000,3)
            return
    elif mainStage == 3:
        retryCommit = 0
        sco = 0
        while (retryCommit < retrymax):
            print(retryCommit)
            sco = setCommit(driver,B1,root,addminutes)
            if sco == 0:
                retryCommit =+ 1
            else:
                break
        if sco == 0:
            status(B1,"Commit err, restarting...")
            cleanup(60000,3)
            return
    elif mainStage == 4:
        status(B1,"Cleaning up")
        cleanup(2000,3)
        return
    main(mainStage + 1)

def cleanup(seconds, option = 0):
    if option == 1:
        root.after(seconds, threadworker(0))
    elif option == 3:
        switchTab(driver, 0)
        closeTab(driver, 2)
        root.after(seconds, threadworker(0))


def threadworker(runtarget = 1):
    global isStopped
    if runtarget == 1:
        isStopped = 0
        status(B2,"Stop",rebuild)
        th = Thread(target=preload)
        th.start()
        th2 = Thread(target=main)
        th2.start()
    else:
        th = Thread(target=main)
        th.start()
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

def rebuild():
    global isStopped
    status(B1,"Stopping...")
    isStopped = 1
    try:
        driver.quit()
    except:
        pass
    status(B1,"Welcome to the commitment automation tool!")
    status(B2,"Start",threadworker)
    #status(B3,"Quit",lambda: end(root,driver))

    autoChk = (ttk.Checkbutton(root,text="Autorun", variable=autorun,command=setAutorunMain))
    autoChk.grid(column=0,row=3)

if startGUI == 0:
    threadworker()
else:
    root = Tk()
    root.title("Commitment Manager")
    root.geometry("250x165")
    if debug == 1:
        root.iconbitmap("assets/Logo_b.ico")
    root.configure(bg=bgc)
    root.grid_columnconfigure(0,weight=1)

    s = ttk.Style()
    s.configure('TFrame',background=bgc)

    frm = ttk.Frame(root, padding=5)
    frm.grid()

    B1 = Label(frm, text="loading...",wraplength=200, justify='center',bg=bgc,fg=fgc,height=2)
    B1.grid(column=0, row=0)

    B2 = tkinter.Button(frm, text="Start",command=threadworker, bg=bgaccent,fg=fgc,width=20,height=2,font=('Arial', 10))
    B2.grid(column=0,row=1)

    B3 = tkinter.Button(frm, text="Quit", command=lambda: end(root,driver), bg=bgaccent,fg=fgc,width=20,height=2,font=('Arial', 10))
    B3.grid(column=0, row=2)
    
    config = getConfig(B1)
    autorun = StringVar(value=config['autorun'])
    print(autorun)
    status(B1,"Welcome to the commitment automation tool!")
    
    autoChk = (tkinter.Checkbutton(root,text="Autorun", variable=autorun,command=setAutorunMain,bg=bgc,fg=fgc,selectcolor=bgc))
    autoChk.grid(column=0,row=3)
    if autorun.get() == "1":
        countdown(5)
    root.mainloop()