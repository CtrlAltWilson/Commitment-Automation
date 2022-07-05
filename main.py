import shutil, errno, json, os
from webbrowser import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

debug = 0
if debug:
    try:
        os.remove('assets\config.json')
    except:
        pass

def errlog(loc):
    print("error in {}".format(loc))

def getConfig():
    try:
        with open('assets\config.json','r') as f:
            config = json.load(f)
    except:
        config = {}
        profileurl = input("Profile URL (can be found from: chrome://version/): ").strip().split('\\')
        config['profile_user'] = profileurl[-1]
        profileurl.pop(-1)
        config['profile_url'] = ("{}\\".format('\\'.join(profileurl)))
        with open('assets\config.json','w') as f:
            json.dump(config, f)
        getConfig()
    return config

def copyprofile(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc:
        if exc.errno in (errno.ENOTDIR, errno.EINVAL):
            shutil.copy(src,dst)
        else:raise

def launchBrowser():
    config = getConfig()
    profilepath = 'assets\\profile\\'
    #if not os.path.isdir(profilepath):
        #print("Please copy profile folder over to assets\\profile")
        #print('copying profile...')
        #sourcepath = '{}{}'.format(config['profile_url'],config['profile_user'])
        #copyprofile(sourcepath, profilepath)
        #print('compelted.')
    #TODO
    chrome_options = Options() #comeback https://www.programcreek.com/python/example/100025/selenium.webdriver.ChromeOptions
    #chrome_options.add_argument('--profile-directory=Profile 10')
    chrome_options.add_argument('user-data-dir={}{}'.format(config['profile_url'],config['profile_user']))
    #chrome_options.add_argument('user-data-dir=Profile 10')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
    driver.get('https://raptor.my.salesforce.com/500?fcf=00BU0000004L8j3')
    while True:
        if "login.microsoftonline" in driver.current_url:
            print("SSO required")
            input("Press Enter to continue...")
        pass
    return

driver = launchBrowser()
