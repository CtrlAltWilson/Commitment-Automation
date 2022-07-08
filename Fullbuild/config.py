import os, json
from updatetk import updatetk as status
from constrants import debug

def getConfig(btn):
    try:
        status(btn,"Getting config file...")
        if debug == 1:
            with open('assets\config.json','r') as f:
                config = json.load(f)
        else:
            with open('config.json','r') as f:
                config = json.load(f)
    except:
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
        
        getConfig(btn)

    status(btn,"Config caught!")
    
    return config

def setAutorun(value):
    if debug == 1:
        with open('assets\config.json','r') as f:
            config = json.load(f)

        config['autorun'] = value

        with open('assets\config.json','w') as f:
            json.dump(config, f)
    else:
        with open('config.json','r') as f:
            config = json.load(f)

        config['autorun'] = value

        with open('config.json','w') as f:
            json.dump(config, f)