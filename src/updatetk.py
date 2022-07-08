import pytz
from datetime import datetime

def updatetk(btn,text,cmd = None):
    if text == "":
        return
    print(text)
    log(text)
    if cmd is None:
        btn.configure(text=text)
    else:
        btn.configure(text=text,command=cmd)

def log(text):
    to_zone = pytz.timezone('America/Chicago')
    now = datetime.now(to_zone)
    new_time = now.strftime("%Y-%d-%m %I:%M %p")
    with open("logs.txt","a") as f:
        f.write("{}: {}\n".format(new_time,text))