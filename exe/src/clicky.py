from selenium import webdriver

def clicky(statusName, driver,click = 2, loc = "id"):
    try:
        action = webdriver.ActionChains(driver)
        status = driver.find_element(loc, statusName)
        #print(status.text)
        if click == 2:
            action.double_click(status).perform()
        else:
            status.click()
        return
    except Exception as functionerr:
        print("CLICKY",str(functionerr))