import os, json
from src.updatetk import updatetk as status

def getConfig(btn):
    try:
        status(btn,"Getting config file...")
        with open('assets\config.json','r') as f:
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
        
        config['autorun'] = True
        with open('assets\config.json','w') as f:
            json.dump(config, f)
        
        getConfig()

    status(btn,"Config caught!")
    
    return config