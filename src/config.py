import os, json
try:
    from src.updatetk import updatetk as status
    from src.constrants import debug
except:
    from updatetk import updatetk as status
    from constrants import debug

def getConfig(btn = None):
    try:
        if btn is not None:
            status(btn,"Getting config file...")
        try:
            with open('assets\config.json','r') as f:
                config = json.load(f)
        except:
            with open('config.json','r') as f:
                config = json.load(f)
    except:
        if btn is not None:
            status(btn,"No config file found! Creating one...")
        default_user = os.getcwd().split("\\")
        default_path = "C:\\Users\\{}\\AppData\\Local\\Google\\Chrome\\User Data\\Default".format(default_user[2])
        
        config = {}

        if os.path.isdir(default_path):
            profileurl = default_path.split('\\')
        else:
            #TODO create input for url
            profileurl = input("Profile URL (can be found from: chrome://version/): ").strip().split('\\')

        config['profile_user'] = profileurl[-1]
        profileurl.pop(-1)
        config['profile_url'] = ("{}\\".format('\\'.join(profileurl)))
        
        config['autorun'] = "0"
        if debug == 1:
            with open('assets\config.json','w') as f:
                json.dump(config, f)
        else:
            with open('config.json','w') as f:
                json.dump(config, f)
        if btn is not None:
            getConfig(btn)
        else:
            getConfig()
    if btn is not None:
        status(btn,"Config caught!")
    
    return config

def setAutorun(value):
    try:
        with open('assets\config.json','r') as f:
            config = json.load(f)

        config['autorun'] = value

        with open('assets\config.json','w') as f:
            json.dump(config, f)
    except:
        with open('config.json','r') as f:
            config = json.load(f)

        config['autorun'] = value

        with open('config.json','w') as f:
            json.dump(config, f)