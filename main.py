import json, os, time, re, pytz

from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select

from webdriver_manager.chrome import ChromeDriverManager

from tkinter import *
from tkinter import ttk

from src.constants import *

#TODO need to fix time sleep freeze

#globals
driver = None
B1 = None
action = None
addminutes = 2
retry = 0
config = None


if debug == 2:
    try:
        os.remove('assets\config.json')
    except:
        pass

#deprecated
def errlog(loc):
    print("error in {}".format(loc))

def getConfig():
    try:
        status_update("Getting config file...")
        with open('assets\config.json','r') as f:
            config = json.load(f)
    except:
        status_update("No config file found! Creating one...")
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

def launchBrowser(headless = 1):
    global driver,B2,retry, action,config
    if debug == 0:
        B2.destroy()
        pause_btn()
    else:
        config = getConfig()
    status_update("Starting...")
    print(config)
    try:
        chrome_options = Options() #comeback https://www.programcreek.com/python/example/100025/selenium.webdriver.ChromeOptions
        chrome_options.add_argument('user-data-dir={}{}'.format(config['profile_url'],config['profile_user']))
        if headless == 1:
            chrome_options.add_argument('--headless')
        chrome_options.add_experimental_option("detach",True)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
        action = webdriver.ActionChains(driver)
        driver.get('https://raptor.my.salesforce.com/500?fcf=00BU0000004L8j3')
    except Exception as e:
        status_update(e)
        time.sleep(5)
        if "unknown error" in str(e):
            status_update("Error: Existing Browser Opened! Retrying...")
            try:
                driver.close()
            except:
                status_update("Failed! Ending...")
                end()
            retry += 1
            if retry == retrymax:
                end()
            time.sleep(2)
            launchBrowser()
            return
    if headless == 1:
        checkSSO()

def waitingRoom(newCases = 1):
    global addminutes
    status_update("Sitting in the waiting room...")
    driver.get("https://raptor.my.salesforce.com/500?fcf=00BU0000004L8j3")
    if newCases == 0:
        time.sleep(60)
    while True:
        busy = checkBusy()
        if busy >= 2:
            addminutes = 2
        else:
            addminutes = 60
            time.sleep(60)
        if "00BU0000004L8j3" in driver.current_url:
            refreshBtn = driver.find_element("id","00BU0000004L8j3_refresh")
            refreshBtn.click()
        else:
            driver.get("https://raptor.my.salesforce.com/500?fcf=00BU0000004L8j3")
        checkCases()
        break

def checkBusy():
    status_update("Checking availability...")
    time.sleep(3)
    driver.switch_to.frame(driver.find_elements("tag name", "iframe")[1])
    agentlist = driver.find_element("id","homeAgentsIconId")
    agentlist.click()
    time.sleep(1)

    filteragents = driver.find_element("class name","filterCombo")
    filteragents.click()
    filteragents2 = driver.find_element("id","Support")
    filteragents2.click()
    counter = 0
    agents = driver.find_elements("id","line1AgentStateId")
    for i in agents:
        #print(i.text)
        if "Available" in i.text:
            counter += 1
    #print(counter)
    return counter

def checkSSO(ctnBtn = None):
    status_update("Checking SSO...")
    time.sleep(1)
    if ctnBtn is not None and not debug:
        ctnBtn.destroy()
        driver.close()
        pause_btn()
        launchBrowser()
    time.sleep(1)
    if "login.microsoftonline" in driver.current_url:
        #print("SSO required")
        status_update("SSO required")
        driver.close()
        continue_btn()
        launchBrowser(0)
    else:
        inBrowser()

def inBrowser(ctnBtn = None):
    if ctnBtn is not None:
        ctnBtn.destroy()
    #print("inBrowser")
    status_update("Browser started!")
    if "00BU0000004L8j3" in driver.current_url:
        checkCases()

def checkCases():
    status_update("Checking Cases...")
    try:
        caselist = driver.find_elements("class name","x-grid3-row-table")
        noNewCases = 0
        for i in caselist:
            #print("getting attributes")
            case_status = i.find_element("class name", "x-grid3-col-CASES_STATUS")
            case_contact = i.find_element("class name", "x-grid3-col-NAME")
            if ("New" in case_status.text) and ("Installation Request" not in case_status.text) and (case_contact.text != " ") and ("delete" not in case_status.text) and ("remove" not in case_status.text):
                case_subject = i.find_element("class name", "x-grid3-col-CASES_SUBJECT")
                case_subject_link = case_subject.find_element("link text", case_subject.text)
                #print(case_status.text)
                #print(case_subject.text)
                case_subject_link.click()
                setNewCase()
                break
            noNewCases = 1
        if noNewCases:
            waitingRoom(0)
    except Exception as e:
        if "cannot determine loading status" in str(e):
            time.sleep(2)
            setNewCase()

def setNewCase():
    status_update("Setting new cases...")
    clicky("cas7_ilecell")
    selecty("cas7","Scheduled Support Call")
    clicky("00N0P000005z2qO_ilecell")
    selecty("00N0P000005z2qO","Support")
    selecty("00N0P000006lfKG","Visitor Management")
    selecty("00N0P000006lfKL","Training_VM")
    selecty("00N0P000006lfKV","Visitor Module")
    okBtn = driver.find_elements("class name", "zen-btn")
    okBtn[0].click()
    getPlatform = driver.find_element("id","00N0P000007X5eZ_ileinner")
    if getPlatform.text == " " or getPlatform.text == None:
        getEmailSubject = driver.find_elements("class name","dataCell")
        company = None
        for i in getEmailSubject:
            #print("Emails {}".format(i.text))
            if "LOBBYGUARD Support Request Received" in i.text:
                company = "LobbyGuard"
                break
        if company is None:
            company = "Raptor 6"
        #print(company)
        clicky("00N0P000007X5eZ_ileinner")
        selecty("00N0P000007X5eZ_unselected",company)
        okBtn = driver.find_elements("class name", "picklistArrowRight")
        okBtn[0].click()
        okBtn = driver.find_elements("class name", "zen-btn")
        okBtn[0].click()
    #else:
        #print(getPlatform.text)
    setCommit()
    saveCase = 'document.querySelector(\'[name=inlineEditSave]\').click()'
    driver.execute_script(saveCase)
    waitingRoom()
    return

def setCommit():
    status_update("Setting Commit...")

    phone = driver.find_element("id","cas20_ileinner")
    if phone.text == " ":
        phone = driver.find_element("id","00N0P000006Fnqk_ileinner")
    phone = phone.text
    phone = phone.strip()
    
    #print("phone0",phone)
    phone = re.sub('[\(\)\-\.\ ]','',phone)
    #print("phone1",phone)
    email = driver.find_element("id","cas10_ileinner")
    email = email.text
    if (phone == "") or ('+' in phone) or (len(phone) < 10) or ("@raptortech.com" in email):
        return
    name = driver.find_element("id","cas3_ileinner")
    name = name.text
    case = driver.find_element("class name", "pageDescription")
    case = case.text
    time.sleep(2)

    status_update("Switching frames")

    radioScript = 'radiobtn = document.querySelectorAll("input[type=radio][name=promiseBtnId]"); radiobtn[1].checked = true;'
    obScript = 'document.querySelector(".txtSpn.textEllipsis.dispComboText").click(); document.querySelector("[id=\'Support OB\']").click();'
    timeclearScript = 'document.querySelector(\'[id=timePickerInputTxt]\').value = ""'
    saveTime = 'document.querySelector(\'[id=saveBtn]\').click();'
    saveCommit = 'document.querySelector(\'[id=saveBtnID]\').click();'

    driver.switch_to.frame(driver.find_elements("tag name", "iframe")[1])
    commitBtn = driver.find_element("id","HomePromiseKeeperIconDiv")
    commitBtn.click()
    time.sleep(1)

    newCommit = driver.find_element("id","newBtnId")
    newCommit.click()
    time.sleep(1)

    driver.find_element("id","firstNameId").send_keys(case)
    driver.find_element("id","lastNameId").send_keys(name)
    driver.find_element("id","phoneId").send_keys(phone)

    driver.execute_script(radioScript)
    time.sleep(1)

    driver.execute_script(obScript)
    driver.find_element("class name","dateTimeIconDiv").click()
    time.sleep(1)

    to_zone = pytz.timezone('America/Chicago')
    now = datetime.now(to_zone) + timedelta(minutes=addminutes)
    new_time = now.strftime("%I:%M %p")
    driver.execute_script(timeclearScript)
    driver.find_element("class name","timePickerOptionsTxt").send_keys(new_time)
    time.sleep(1)

    driver.execute_script(saveTime)
    time.sleep(1)

    driver.execute_script(saveCommit)
    status_update("Returning frames")

    driver.switch_to.default_content()
    return

def clicky(statusName, click = 2, loc = "id"):
    status = driver.find_element(loc, statusName)
    #print(status.text)
    if click == 2:
        action.double_click(status).perform()
    else:
        status.click()
    return

def selecty(idName,valueName):
    select = Select(driver.find_element("id",idName))
    select.select_by_visible_text(valueName)
    return

def status_update(newmsg):
    print(newmsg)
    if debug:
        return
    global B1
    B1.destroy()
    B1 = ttk.Label(frm, text=newmsg,wraplength=200, justify='center')
    B1.grid(column=0,row=0)
    frm.update()

def pause_btn():
    if debug:
        return
    ctnBtn = ttk.Button(frm, text="Pause",command=lambda: continue_btn(ctnBtn))
    ctnBtn.grid(column=0,row=1)
    frm.update()

def continue_btn(btn = None):
    if debug:
        return
    if btn is not None:
        btn.destroy()
        status_update("Paused")
    ctnBtn = ttk.Button(frm, text="Continue",command=lambda: checkSSO(ctnBtn))
    ctnBtn.grid(column=0,row=1)
    frm.update()

def end():
    if debug:
        return
    global root
    status_update("Goodbye!")
    if driver is not None:
        try:
            driver.close()
        except:
            pass
    root.after(1,root.destroy())

if debug == 1:
    driver = launchBrowser()
else:
    root = Tk()
    root.geometry("250x100")
    root.grid_columnconfigure(0,weight=1)
    frm = ttk.Frame(root, padding=5)
    frm.grid()
    B1 = ttk.Label(frm, text="loading...",wraplength=200, justify='center')
    B1.grid(column=0, row=0)
    config = getConfig()
    status_update("Welcome to the commitment automation tool!")

    B2 = ttk.Button(frm, text="Start",command=launchBrowser)
    B2.grid(column=0,row=1)

    B3 = ttk.Button(frm, text="Quit", command=end)
    B3.grid(column=0, row=2)
    root.mainloop()
    root.update()
