from selenium.webdriver.support.ui import Select

def selecty(idName,valueName,driver):
    try:
        select = Select(driver.find_element("id",idName))
        select.select_by_visible_text(valueName)
        return
    except Exception as functionerr:
        print(functionerr)