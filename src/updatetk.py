
def updatetk(btn,text,cmd = None):
    if text == "":
        return
    print(text)
    if cmd is None:
        btn.configure(text=text)
    else:
        btn.configure(text=text,command=cmd)
    