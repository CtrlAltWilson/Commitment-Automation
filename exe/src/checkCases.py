from src.updatetk import updatetk as status
from src.tabs import switchTab
from src.constrants import retrymax

def checkCases(driver,btn,root):
    retry = 0
    switchTab(driver,0)
    refreshScript = "document.querySelectorAll('[class=lastItem]')[0].querySelector('input[type=button]').click()"
    while (retry < retrymax):
        try:
            status(btn,"Checking Cases...")
            driver.execute_script(refreshScript)
            root.after(2000, status(btn,""))
            caselist = driver.find_elements("class name","x-grid3-row-table")
            for i in caselist:
                case_status = i.find_element("class name", "x-grid3-col-CASES_STATUS")
                case_contact = i.find_element("class name", "x-grid3-col-NAME")
                case_email = i.find_element("class name","x-grid3-td-CASES_EMAIL")
                if ("New" in case_status.text) and ("Installation Request" not in case_status.text) and \
                    (case_contact.text != " ") and ("delete" not in case_status.text) and \
                        ("remove" not in case_status.text) and ("@raptortech.com" not in case_email.text) and \
                            ("@lobbyguard.com" not in case_email.text):
                    case_subject = i.find_element("class name", "x-grid3-col-CASES_SUBJECT")
                    case_subject_link = case_subject.find_element("link text", case_subject.text)
                    return case_subject_link.get_attribute('href')
            return 0
        except Exception as functionerr:
            print("CHECKCASES",functionerr)
        retry += 1
    return 0