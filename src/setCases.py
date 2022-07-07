from src.updatetk import updatetk as status
from src.constrants import retrymax
from src.clicky import clicky
from src.selecty import selecty

def setNewCase(root,btn,driver):
    retry = 0
    while(retry < retrymax):
        try:
            root.after(5000, status(btn,""))
            status(btn,"Setting new cases...")
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
            print("SETNEWCASES",str(functionerr))
        retry += 1
    return 0