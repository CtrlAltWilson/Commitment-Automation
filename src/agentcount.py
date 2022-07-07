from src.constrants import retrymax,sfAgentlink, debug
from src.updatetk import updatetk as status
from src.tabs import switchTab

def agentCount(driver,root,btn):
    retry = 0
    switchTab(driver,1)
    driver.get(sfAgentlink)
    while (retry < retrymax):
        try:
            root.after(10000, status(btn,"Checking availability..."))
            agentlist = driver.find_element("id","homeAgentsIconId")
            agentlist.click()
            root.after(1000, status(btn,""))
            filteragents = driver.find_element("class name","filterCombo")
            filteragents.click()
            filteragents2 = driver.find_element("id","Support")
            filteragents2.click()
            counter = 0
            agents = driver.find_elements("id","line1AgentStateId")
            for i in agents:
                if "Available" in i.text:
                    counter += 1
            status(btn,"{} available agents".format(counter))
            driver.get(sfAgentlink)
            return counter
        except Exception as functionerr:
            if "Unable to locate element" in str(functionerr):
                print("Page didn't load, reloading")
                driver.get(sfAgentlink)
                root.after(3000, status(btn,""))
            else:
                print("AGENT COUNT",str(functionerr))
        retry += 1
    if debug == 1:
        return 1
    return 0