import re, pytz

from datetime import datetime, timedelta

from src.updatetk import updatetk as status
from src.tabs import switchTab
from src.constrants import debug, retry, retrymax, driver, root, B1, addminutes

radioScript = 'radiobtn = document.querySelectorAll("input[type=radio][name=promiseBtnId]"); radiobtn[1].checked = true;'
obScript = 'document.querySelector(".txtSpn.textEllipsis.dispComboText").click(); document.querySelector("[id=\'Support OB\']").click();'
timeclearScript = 'document.querySelector(\'[id=timePickerInputTxt]\').value = ""'
saveTime = 'document.querySelector(\'[id=saveBtn]\').click();'
saveCommit = 'document.querySelector(\'[id=saveBtnID]\').click();'

def setCommit(d, btn,r,am):
    global driver, root, B1, addminutes
    driver = d
    root = r
    B1 = btn
    addminutes = am
    root.after(50, stage1)

def stage1():
    try:
        status(B1,"Setting Commit...")

        phone = driver.find_element("id","cas20_ileinner")
        if phone.text == " ":
            phone = driver.find_element("id","00N0P000006Fnqk_ileinner")
        phone = phone.text
        phone = phone.strip()
        
        phone = re.sub('[\(\)\-\.\ ]','',phone)
        email = driver.find_element("id","cas10_ileinner")
        email = email.text
        if (phone == "") or ('+' in phone) or (len(phone) < 10) or ("@raptortech.com" in email):
            return 0
        name = driver.find_element("id","cas3_ileinner")
        name = name.text
        case = driver.find_element("class name", "pageDescription")
        case = case.text
        root.after(2000, stage2(case,name,phone))
    except Exception as e:
        onErr(e)

def stage2(case,name,phone):
    try:
        status(B1,case)
        status(B1,"Switching frames")



        switchTab(driver,1)
        #deprecated
        #driver.switch_to.frame(driver.find_elements("tag name", "iframe")[1])
        commitBtn = driver.find_element("id","HomePromiseKeeperIconDiv")
        commitBtn.click()
        root.after(1000, stage3(case,name,phone))
    except Exception as e:
        onErr(e)

def stage3(case,name,phone):
    try:
        newCommit = driver.find_element("id","newBtnId")
        newCommit.click()
        root.after(1000, stage3_5(case,name,phone))
    except Exception as e:
        onErr(e)

def stage3_5(case,name,phone):
    try:
        driver.find_element("id","firstNameId").send_keys(case)
        driver.find_element("id","lastNameId").send_keys(name)
        driver.find_element("id","phoneId").send_keys(phone)

        driver.execute_script(radioScript)
        root.after(1000, stage4)
    except Exception as e:
        onErr(e)

def stage4():
    try:
        driver.execute_script(obScript)
        driver.find_element("class name","dateTimeIconDiv").click()
        root.after(1000, stage5)
    except Exception as e:
        onErr(e)

def stage5():
    try:
        to_zone = pytz.timezone('America/Chicago')
        now = datetime.now(to_zone) + timedelta(minutes=addminutes)
        new_time = now.strftime("%I:%M %p")
        driver.execute_script(timeclearScript)
        driver.find_element("class name","timePickerOptionsTxt").send_keys(new_time)
        root.after(1000, stage6)
    except Exception as e:
        onErr(e)
def stage6():
    try:
        driver.execute_script(saveTime)
        root.after(1000, stage7)
    except Exception as e:
        onErr(e)

def stage7():
    try:
        driver.execute_script(saveCommit)
        status(B1,"Returning frames")
        return 1
    except Exception as e:
        onErr(e)
        
def onErr(functionerr):
    if debug == 1:
        print("SETCOMMIT",str(functionerr))
    status(B1,"Set Commit Error")
    retryFunc()

def retryFunc():
    global retry
    retry += 1
    if retry == retrymax:
        return 0
    else:
        driver.get(driver.current_url)
        root.after(10000,stage1)