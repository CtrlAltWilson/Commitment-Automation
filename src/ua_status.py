from time import sleep

try:
    from src.constrants import sfAgentlink,retry,retrymax
    from src.tabs import switchTab
except:
    from constrants import sfAgentlink,retry,retrymax
    from tabs import switchTab

js_script = \
    "if (document.querySelector(\'[id=stateDescId]\').textContent == \'Unavailable\'){ \
	document.querySelector(\'[id=cStatePanelId]\').click(); \
	document.querySelector(\'[id=agentStates_12]\').click(); \
    };"
js1 = "document.querySelector(\'[id=cStatePanelId]\').click();"
js2 = "document.querySelector(\'[id=agentStates_12]\').click();"

def check_unavail(driver,test = 0):
    global retry
    if test == 0:
        switchTab(driver,1)
    #driver.get(sfAgentlink)
    try:
        while driver.find_element("id","stateDescId").text and retry < retrymax:
            try:
                #print(driver.find_element("id","stateDescId").text)
                if "Unavailable" in driver.find_element("id","stateDescId").text:
                    driver.execute_script(js1)
                    driver.execute_script(js2)
                    break
            except:
                driver.get(sfAgentlink)
            retry +=1
    except:
        pass