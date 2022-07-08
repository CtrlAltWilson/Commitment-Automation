from updatetk import updatetk as status
from constrants import retrymax
from clicky import clicky
from selecty import selecty
from constrants import debug

def setNewCase(root,btn,driver):
    retry = 0
    while(retry < retrymax):
        try:
            root.after(5000, status(btn,""))
            status(btn,"Setting new cases...")
            case = driver.find_element("class name", "pageDescription")
            case = case.text
            status(btn, "Case: {}".format(case))
            clicky("cas7_ilecell",driver)
            root.after(2000, status(btn,""))
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
            if debug == 1:
                print("SETNEWCASES",str(functionerr))
            status(btn, "SetCases Error")
        retry += 1
    return 0