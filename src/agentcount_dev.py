from src.constrants import retrymax,sfAgentlink, debug,driver, root, B1, retry
from src.updatetk import updatetk as status
from src.tabs import switchTab

def agentCount(d,r,btn):
    global driver, root, B1

    if debug == 1:
        return 1

    driver = d
    root = r
    B1 = btn

    switchTab(driver,1)
    driver.get(sfAgentlink)
    status(B1,"Starting agent count")
    root.after(10000, start)


def start():
    status(B1,"Checking availability...")
    try:
        agentlist = driver.find_element("id","homeAgentsIconId")
        agentlist.click()
        root.after(1000, stage2)
    except Exception as functionerr:
        onErr(functionerr)

def stage2():
    try:
        filteragents = driver.find_element("class name","filterCombo")
        filteragents.click()
        filteragents2 = driver.find_element("id","Support")
        filteragents2.click()
        counter = 0
        agents = driver.find_elements("id","line1AgentStateId")
        for i in agents:
            if "Available" in i.text:
                counter += 1
        status(B1,"{} available agents".format(counter))
        driver.get(sfAgentlink)
        return counter
    except Exception as functionerr:
        onErr(functionerr)

def onErr(functionerr):
    if "Unable to locate element" in str(functionerr):
        if debug == 1:
            print("Page didn't load, reloading")
        status(B1, "Page didn't load, reloading")
    else:
        if debug == 1:
            print("AGENT COUNT",str(functionerr))
    status(B1,"Agent Count Error")
    retryFunc()

def retryFunc():
    global retry
    retry += 1
    if retry == retrymax:
        return 0
    else:
        switchTab(driver,1)
        driver.get(sfAgentlink)
        root.after(10000,start)
