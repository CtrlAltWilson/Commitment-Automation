import os

def end(root, driver = None):
    try:
        #status_update("Goodbye!")
        if driver is not None:
            try:
                driver.quit()
            except:
                pass
        root.after(1,root.destroy())
    except Exception as functionerr:
        #print(functionerr)
        pass
    try:
        os.system('cmd taskkill /f /im cmtmgr.exe')
    except: 
        pass