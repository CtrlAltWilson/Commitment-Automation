import os
try:
    from src.constrants import getver,debug,noconsole
except:
    from constrants import getver,debug,noconsole


def end(root, driver = None):
    global getver
    if debug == 1:
        getver.append("beta")
    if noconsole == 0:
        getver.append("dev")


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
        os.system('cmd /c taskkill /f /im cmtmgr_{}.exe'.format("_".join(getver)))
    except: 
        pass