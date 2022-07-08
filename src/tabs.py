try:
    from src.constrants import sfAgentlink
except:
    from constrants import sfAgentlink

def defaultTabs(driver):
    driver.execute_script("window.open()")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(sfAgentlink)

def createTab(driver,link):
    driver.execute_script("window.open()")
    driver.switch_to.window(driver.window_handles[2])
    driver.get(link)

def closeTab(driver,tab: int):
    driver.switch_to.window(driver.window_handles[tab])
    driver.close()

def switchTab(driver,tab: int):
    try:
        driver.switch_to.window(driver.window_handles[tab])
    except:
        print("No tabs")
        return