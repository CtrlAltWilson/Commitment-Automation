from tkinter import *
from tkinter import ttk

from threading import *
import tkinter
import webbrowser
try:
    from src.end import end
    from src.browser import mainLaunch
    from src.updatetk import updatetk as status
    from src.config import getConfig, setAutorun
    from src.tabs import createTab, defaultTabs, closeTab, switchTab
    from src.constrants import  \
        action,             \
        addminutes,         \
        autorun,            \
        bgaccent,           \
        bgc,                \
        commitscreated,     \
        debug,              \
        driver,             \
        finished,           \
        fgc,                \
        isStopped,          \
        startGUI,           \
        version            \

    from src.agentcount import agentCount
    from src.checkCases import checkCases
    from src.setCommit import setCommit
    from src.setCases import setNewCase
    from src.ua_status import check_unavail
except:
    from end import end
    from browser import mainLaunch
    from updatetk import updatetk as status
    from config import getConfig, setAutorun
    from tabs import createTab, defaultTabs, closeTab, switchTab
    from constrants import  \
        action,             \
        addminutes,         \
        autorun,            \
        bgaccent,           \
        bgc,                \
        commitscreated,     \
        debug,              \
        driver,             \
        finished,           \
        fgc,                \
        isStopped,          \
        startGUI,           \
        version            \
        

    from agentcount import agentCount
    from checkCases import checkCases
    from setCommit import setCommit
    from setCases import setNewCase
    from ua_status import check_unavail

#TODO
#prin out to txt logs
#threading?
#check logged in/out
#set different statuses

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
    global addminutes, commitscreated
    while finished == False:
        pass
    if isStopped == 1:
        return
    elif mainStage == 0:
        ac = agentCount(driver,root,B1)
        status(B4,"Agents: {}".format(ac+1))
        #print(ac)
        #should probably recheck this
        if ac > 1:
            addminutes = 2
        else:
            addminutes = 60
    elif mainStage == 1:
        cc = checkCases(driver,B1, root)
        if cc == 0:
            status(B1,"No cases found, sleeping...")
            cleanup(60000,1)
            return
        print("cc",cc)
        createTab(driver,cc)
    elif mainStage == 2:
        sc = setNewCase(root,B1,driver)
        if sc == 0:
            status(B1,"Case err, restarting...")
            cleanup(60000,3)
            return
    elif mainStage == 3:
        sco = setCommit(driver,B1,root,addminutes)
        commitscreated += 1
        if sco == 0:
            status(B1,"Commit err, restarting...")
            cleanup(60000,3)
            return
    elif mainStage == 4:
        status(B1,"Cleaning up")
        cleanup(2000,3)
        return
    root.after(250,main(mainStage + 1))

def cleanup(seconds, option = 0):
    status(B5,"Created: {}".format(commitscreated))
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
    global isStopped
    isStopped = 0
    print("Writing to config") 
    print(autorun.get())

    setAutorun(autorun.get())
    config['autorun'] = autorun.get()
    if autorun.get() == "1":
        status(B2,"Stop",rebuild)
        countdown(5)
    else:
        status(B2,"Start",threadworker)

def countdown(count):
    if isStopped == 1:
        return
    status(B1,str(count))
    if count > 0:
        if autorun.get() == "0":
            status(B1,"Welcome to the commitment automation tool!")
            setAutorunMain()
            return
        # call countdown again after 1000ms (1s)
        root.after(1000, countdown, count-1)
    else:
        if autorun.get() == "1" and isStopped == 0:
            threadworker()
        else:
            return

def rebuild():
    global isStopped
    status(B1,"Stopping...")
    status(B4,"py.wilsonngo.com")
    isStopped = 1
    try:
        driver.quit()
    except:
        pass
    status(B1,"Welcome to the commitment automation tool!")
    status(B2,"Start",threadworker)
    #status(B3,"Quit",lambda: end(root,driver))

    autoChk = (tkinter.Checkbutton(root,text="Autorun", variable=autorun,command=setAutorunMain,bg=bgc,fg=fgc,selectcolor=bgc))
    autoChk.grid(column=0,row=3)

def callback(url):
    webbrowser.open_new(url)

if startGUI == 0:
    threadworker()
else:
    root = Tk()
    root.title("Commitment Manager")
    root.geometry("250x200")
    
    """
    #TODO
    try:
        root.iconbitmap("assets/Logo_b.ico")
    except:
        root.iconbitmap("Logo_b.ico")
    """

    root.configure(bg=bgc)
    root.grid_columnconfigure(0,weight=1)

    s = ttk.Style()
    s.configure('TFrame',background=bgc)

    frm = ttk.Frame(root, padding=5)
    frm.grid()

    B1 = Label(
        frm, 
        text="loading...",
        wraplength=200, 
        justify='center',
        bg=bgc,
        fg=fgc,
        height=2
        )
    B1.grid(column=0, row=0)

    B2 = tkinter.Button(
        frm, 
        text="Start",
        command=threadworker, 
        bg=bgaccent,
        fg=fgc,
        width=20,
        height=2,
        font=('Arial', 10)
        )
    B2.grid(column=0,row=1)

    B3 = tkinter.Button(
        frm, 
        text="Quit", 
        command=lambda: end(root,driver), 
        bg=bgaccent,
        fg=fgc,
        width=20,
        height=2,
        font=('Arial', 10)
        )
    B3.grid(column=0, row=2)

    config = getConfig(B1)
    autorun = StringVar(value=config['autorun'])
    if debug == 1:
        print(autorun.get())
    status(B1,"Welcome to the commitment automation tool!")
    
    autoChk = tkinter.Checkbutton(
            root,text="Autorun", 
            variable=autorun,
            command=setAutorunMain,
            bg=bgc,
            fg=fgc,
            selectcolor=bgc,
            height=0
            )
    autoChk.grid(column=0,row=3)

    B4 = Label(
        frm, 
        text="py.wilsonngo.com",
        wraplength=200, 
        justify='center',
        bg=bgc,
        fg=fgc
        )
    B4.grid(column=0, row=4)
    B4.bind("<Button-1>",lambda e: callback("https://py.wilsonngo.com"))

    if debug == 1:
        version = str(version) + " BETA"

    B5 = Label(
        frm, 
        text="VERSION: {}".format(version),
        wraplength=200, 
        justify='center',
        bg=bgc,
        fg=fgc,
        font=('Arial', 7)
        )
    B5.grid(column=0, row=5, ipady=0)

    if autorun.get() == "1":
        status(B2,"Stop",rebuild)
        countdown(5)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        root.destroy()
