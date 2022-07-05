import shutil, errno, json, os
from webbrowser import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from tkinter import *
from tkinter import ttk

debug = 0
if debug:
    try:
        os.remove('assets\config.json')
    except:
        pass

def errlog(loc):
    print("error in {}".format(loc))

def getConfig():
    try:
        with open('assets\config.json','r') as f:
            config = json.load(f)
    except:
        default_user = os.getcwd().split("\\")
        default_path = "C:\\Users\\{}\\AppData\\Local\\Google\\Chrome\\User Data\\Default".format(default_user[2])
        
        config = {}

        if os.path.isdir(default_path):
            profileurl = default_path.split('\\')
        else:
            profileurl = input("Profile URL (can be found from: chrome://version/): ").strip().split('\\')

        config['profile_user'] = profileurl[-1]
        profileurl.pop(-1)
        config['profile_url'] = ("{}\\".format('\\'.join(profileurl)))
        
        with open('assets\config.json','w') as f:
            json.dump(config, f)
        
        getConfig()
    
    return config

def launchBrowser(B1,B2):
    B1.destroy()
    B2.destroy()
    config = getConfig()
    status_update("starting...")
    chrome_options = Options() #comeback https://www.programcreek.com/python/example/100025/selenium.webdriver.ChromeOptions
    chrome_options.add_argument('user-data-dir={}{}'.format(config['profile_url'],config['profile_user']))
    chrome_options.add_experimental_option("detach",True)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
    driver.get('https://raptor.my.salesforce.com/500?fcf=00BU0000004L8j3')
    checkSSO(driver)

def checkSSO(driver, ctnBtn = None):
    if not ctnBtn == None:
        ctnBtn.destroy()
    if "login.microsoftonline" in driver.current_url:
        print("SSO required")
        status_update("SSO required")
        continue_btn(driver)
    else:
        inBrowser(driver)

def inBrowser(driver,ctnBtn = None):
    if not ctnBtn == None:
        ctnBtn.destroy()
    print("inBrowser")
    status_update("Browser started!")

#driver = launchBrowser()

def status_update(the_message):
    statusLbl = ttk.Label(frm, text=the_message)
    statusLbl.grid(column=0,row=0)
    frm.update()
    return statusLbl

def continue_btn(driver):
    ctnBtn = ttk.Button(frm, text="Continue",command=lambda: checkSSO(driver,ctnBtn))
    ctnBtn.grid(column=0,row=1)
    frm.update()

root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
B1 = ttk.Label(frm, text="Hello")
B1.grid(column=0, row=0)

B2 = ttk.Button(frm, text="Start",command=lambda: launchBrowser(B1,B2))
B2.grid(column=0,row=1)

B3 = ttk.Button(frm, text="Quit", command=root.destroy)
B3.grid(column=0, row=2)
root.mainloop()