from src.updatetk import updatetk as status
from src.constrants import retrymax, retry, B1, root, driver
from src.clicky import clicky
from src.selecty import selecty
from src.constrants import debug

def setNewCase(r,btn,d):
    global driver, B1, root
    driver = d
    root = r
    B1 = btn

    root.after(5000, stage1)

def stage1():
    try:
        status(B1,"Setting new cases...")
        case = driver.find_element("class name", "pageDescription")
        case = case.text
        status(B1, "Case: {}".format(case))
        clicky("cas7_ilecell",driver)
        root.after(2000, stage2)
    except Exception as functionerr:
        onErr(functionerr)

def stage2():
    try:
        selecty("cas7","Scheduled Support Call",driver)
        clicky("00N0P000005z2qO_ilecell",driver)
        selecty("00N0P000005z2qO","Support",driver)
        selecty("00N0P000006lfKG","Visitor Management",driver)
        selecty("00N0P000006lfKL","Training_VM",driver)
        selecty("00N0P000006lfKV","Visitor Module",driver)
        okBtn = driver.find_elements("class name", "zen-btn")
        okBtn[0].click()
        getPlatform = driver.find_element("id","00N0P000007X5eZ_ileinner")
        if getPlatform.text == " " or getPlatform.text == None:
            getEmailSubject = driver.find_elements("class name","dataCell")
            company = None
            for i in getEmailSubject:
                if "LOBBYGUARD Support Request Received" in i.text:
                    company = "LobbyGuard"
                    break
            if company is None:
                company = "Raptor 6"
            clicky("00N0P000007X5eZ_ileinner",driver)
            selecty("00N0P000007X5eZ_unselected",company,driver)
            okBtn = driver.find_elements("class name", "picklistArrowRight")
            okBtn[0].click()
            okBtn = driver.find_elements("class name", "zen-btn")
            okBtn[0].click()
        saveCase = 'document.querySelector(\'[name=inlineEditSave]\').click()'
        driver.execute_script(saveCase)
        return 1
    except Exception as functionerr:
        onErr(functionerr)

def onErr(functionerr):
    if debug == 1:
        print("SETNEWCASES",str(functionerr))
    status(B1, "SetCases Error")
    retryFunc()

def retryFunc():
    global retry
    retry += 1
    if retry == retrymax:
        return 0
    else:
        driver.get(driver.current_url)
        root.after(10000,stage1)