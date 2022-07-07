from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from src.constrants import debug, retrymax, driver,caseLink
from src.updatetk import updatetk as status

def mainLaunch(root,config,driver2,btn):
    global driver
    driver = driver2
    try:
        while True:
            chk1 = launchBrowser(root,config,btn)
            chk2 = checkSSO(root, btn)
            print(chk1,chk2)
            if chk1 == -1 or chk2 == -1:
                print("BORKED")
                return -1
            if chk2 == 0: #SSO needed
                chk1 = launchBrowser(root,config,btn,0)
                chk2 = checkSSO(root, btn,0)
            if chk2 == 1:
                break
    except Exception as e:
        print("MAINLAUNCH",str(e))
    if debug == 1:
        driver = launchBrowser(root,config,btn,0,1)
    else:
        driver = launchBrowser(root,config,btn,1,1)
    chk3 = inBrowser(btn)
    if chk3 == 1:
        return driver
    else:
        return -1

def launchBrowser(root,config,btn,headless = 1,getDriver = 0):
    global driver
    if headless == 1:
        status(btn,"Starting browser")

    retry = 0

    while (retry < retrymax):
        try: #Open Browser
            chrome_options = Options()
            chrome_options.add_argument('user-data-dir={}{}'.format(config['profile_url'],config['profile_user']))
            if headless == 1:
                chrome_options.add_argument('--headless')
            chrome_options.add_experimental_option("detach",True)
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
            driver.get(caseLink)
            if getDriver == 1:
                return driver
            else:
                return 1
        except Exception as e:
            print("LAUNCHBROWSER",str(e))
            root.after(5000, status(btn,""))
            if "unknown error" in str(e):
                status(btn,"Error: Existing Browser Opened! Retrying...")
                try:
                    driver.close()
                except:
                    pass
                root.after(2000, status(btn,""))
            else:
                print(str(e))
        retry += 1
        print("Retrying")
    status(btn,"Failed retries with browser")
    return -1

def checkSSO(root,btn,headless = 1):
    try:
        status(btn,"Checking SSO...")
        root.after(1000, status(btn,""))
        if headless == 0:
            while "login.microsoftonline" in driver.current_url:
                root.after(2000, status(btn,""))
            driver.close()
            return 1
        if "login.microsoftonline" in driver.current_url:
            status(btn,"SSO required")
            return 0
    except Exception as functionerr:
        print("SSO",functionerr)
    return 1

def inBrowser(btn1):
    retry = 0
    while (retry < retrymax):
        try:
            status(btn1,"Browser started!")
            if "00BU0000004L8j3" not in driver.current_url:
                driver.get(caseLink)
            return 1
        except Exception as functionerr:
            print("INBROWSER",functionerr)
        retry += 1
    return -1
