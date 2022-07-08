from webbrowser import get
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

try:
    from src.constrants import sfAgentlink,driver,config
    from src.config import getConfig
except:
    from constrants import sfAgentlink,driver
    from config import getConfig

from ua_status import check_unavail

def test():
    global driver, config
    try:
        config = getConfig()

        chrome_options = Options()
        chrome_options.add_argument('user-data-dir={}{}'.format(config['profile_url'],config['profile_user']))
        chrome_options.add_experimental_option("detach",True)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
    except Exception as e:
        print("TEST",str(e))
        #driver.close()
        
        #test()
    time.sleep(10)
    start()

def start():
    driver.get(sfAgentlink)
    check_unavail(driver, 1)
    #pass

test()