from src.updatetk import updatetk as status
from src.tabs import switchTab
from src.constrants import retry,retrymax, debug,driver,B1,root

refreshScript = "document.querySelectorAll('[class=lastItem]')[0].querySelector('input[type=button]').click()"

def checkCases(d,btn,r):
    global driver, root, B1
    driver = d
    root = r
    B1 = btn

    status(B1,"Starting check cases")
    root.after(250, stage1)

def stage1():
    try:
        switchTab(driver,0)
        status(B1,"Checking Cases...")    
        driver.execute_script(refreshScript)
        root.after(2000, stage2)
    except Exception as functionerr:
        onErr(functionerr)

def stage2():
    try:
        caselist = driver.find_elements("class name","x-grid3-row-table")
        for i in caselist:
            case_status = i.find_element("class name", "x-grid3-col-CASES_STATUS")
            case_contact = i.find_element("class name", "x-grid3-col-NAME")
            case_email = i.find_element("class name","x-grid3-col-00N0P000006Fnqp")
            if ("New" in case_status.text) and ("Installation Request" not in case_status.text) and \
                (case_contact.text != " ") and ("delete" not in case_status.text.casefold()) and \
                    ("remove" not in case_status.text.casefold()) and ("@raptortech.com" not in case_email.text) and \
                        ("@lobbyguard.com" not in case_email.text):
                case_subject = i.find_element("class name", "x-grid3-col-CASES_SUBJECT")
                case_subject_link = case_subject.find_element("link text", case_subject.text)
                return case_subject_link.get_attribute('href')
        return 0
    except Exception as funtionerr:
        onErr(funtionerr)

def onErr(functionerr):
    if debug == 1:
        print("CHECKCASES",str(functionerr))
    status(B1,"Check Cases Error")
    retryFunc()

def retryFunc():
    global retry
    retry += 1
    if retry == retrymax:
        return 0
    else:
        root.after(10000,stage1)