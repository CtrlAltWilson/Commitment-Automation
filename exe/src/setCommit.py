import re, pytz

from datetime import datetime, timedelta

from src.updatetk import updatetk as status
from src.tabs import switchTab

def setCommit(driver, btn,root,addminutes):
    try:
        status(btn,"Setting Commit...")

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
        root.after(2000, status(btn,""))

        status(btn,"Switching frames")

        radioScript = 'radiobtn = document.querySelectorAll("input[type=radio][name=promiseBtnId]"); radiobtn[1].checked = true;'
        obScript = 'document.querySelector(".txtSpn.textEllipsis.dispComboText").click(); document.querySelector("[id=\'Support OB\']").click();'
        timeclearScript = 'document.querySelector(\'[id=timePickerInputTxt]\').value = ""'
        saveTime = 'document.querySelector(\'[id=saveBtn]\').click();'
        saveCommit = 'document.querySelector(\'[id=saveBtnID]\').click();'

        switchTab(driver,1)
        #deprecated
        #driver.switch_to.frame(driver.find_elements("tag name", "iframe")[1])
        commitBtn = driver.find_element("id","HomePromiseKeeperIconDiv")
        commitBtn.click()
        root.after(1000, status(btn,""))

        newCommit = driver.find_element("id","newBtnId")
        newCommit.click()
        root.after(1000, status(btn,""))

        driver.find_element("id","firstNameId").send_keys(case)
        driver.find_element("id","lastNameId").send_keys(name)
        driver.find_element("id","phoneId").send_keys(phone)

        driver.execute_script(radioScript)
        root.after(1000, status(btn,""))

        driver.execute_script(obScript)
        driver.find_element("class name","dateTimeIconDiv").click()
        root.after(1000, status(btn,""))

        to_zone = pytz.timezone('America/Chicago')
        now = datetime.now(to_zone) + timedelta(minutes=addminutes)
        new_time = now.strftime("%I:%M %p")
        driver.execute_script(timeclearScript)
        driver.find_element("class name","timePickerOptionsTxt").send_keys(new_time)
        root.after(1000, status(btn,""))

        driver.execute_script(saveTime)
        root.after(1000, status(btn,""))

        driver.execute_script(saveCommit)
        status(btn,"Returning frames")

        return 1
    except Exception as functionerr:
        print("SETCOMMIT",str(functionerr))
        return 0