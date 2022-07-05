import shutil, errno, json, os
from webbrowser import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from tkinter import *
from tkinter import ttk

debug = 0
driver = None
if debug:
    try:
        os.remove('assets\config.json')
    except:
        pass

#deprecated
def errlog(loc):
    print("error in {}".format(loc))

def getConfig():
    try:
        #status_update("Getting config file...")
        with open('assets\config.json','r') as f:
            config = json.load(f)
    except:
        #status_update("No config file found! Creating one...")
        default_user = os.getcwd().split("\\")
        default_path = "C:\\Users\\{}\\AppData\\Local\\Google\\Chrome\\User Data\\Default".format(default_user[2])
        
        config = {}

        if os.path.isdir(default_path):
            profileurl = default_path.split('\\')
        else:
            #TODO create input for url
            profileurl = input("Profile URL (can be found from: chrome://version/): ").strip().split('\\')

        config['profile_user'] = profileurl[-1]
        profileurl.pop(-1)
        config['profile_url'] = ("{}\\".format('\\'.join(profileurl)))
        
        config['autorun'] = True
        with open('assets\config.json','w') as f:
            json.dump(config, f)
        
        getConfig()
    
    return config

def launchBrowser():
    global driver,B2
    B2.destroy()
    status_update("Starting...")
    try:
        chrome_options = Options() #comeback https://www.programcreek.com/python/example/100025/selenium.webdriver.ChromeOptions
        chrome_options.add_argument('user-data-dir={}{}'.format(config['profile_url'],config['profile_user']))
        chrome_options.add_experimental_option("detach",True)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
        driver.get('https://raptor.my.salesforce.com/500?fcf=00BU0000004L8j3')
        checkSSO()
    except:
        status_update("Error: Existing Browser Opened! Retrying...")
        try:
            driver.close()
        except:
            status_update("Failed! Ending...")
            end()
        launchBrowser()

def checkSSO(ctnBtn = None):
    if not ctnBtn == None:
        ctnBtn.destroy()
    if "login.microsoftonline" in driver.current_url:
        print("SSO required")
        status_update("SSO required")
        continue_btn()
    else:
        inBrowser()

def inBrowser(ctnBtn = None):
    if ctnBtn is not None:
        ctnBtn.destroy()
    print("inBrowser")
    status_update("Browser started!")

#driver = launchBrowser()

def status_update(newmsg):
    global B1
    B1.destroy()
    B1 = ttk.Label(frm, text=newmsg,wraplength=200, justify='center')
    B1.grid(column=0,row=0)
    frm.update()

def continue_btn():
    ctnBtn = ttk.Button(frm, text="Continue",command=lambda: checkSSO(ctnBtn))
    ctnBtn.grid(column=0,row=1)
    frm.update()

def end():
    global root
    status_update("Goodbye!")
    if driver is not None:
        try:
            driver.close()
        except:
            pass
    root.after(1,root.destroy())

root = Tk()
root.geometry("250x100")
root.grid_columnconfigure(0,weight=1)
frm = ttk.Frame(root, padding=5)
frm.grid()
config = getConfig()
B1 = ttk.Label(frm, text="Welcome to the commitment automation tool!",wraplength=200, justify='center')
B1.grid(column=0, row=0)

B2 = ttk.Button(frm, text="Start",command=launchBrowser)
B2.grid(column=0,row=1)

B3 = ttk.Button(frm, text="Quit", command=end)
B3.grid(column=0, row=2)
root.mainloop()
root.update()
