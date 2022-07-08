
def timer(root,seconds,cmd = None):
    if seconds > 0:
        root.after(1000, timer(root,seconds-1,cmd))
    else:
        if cmd is not None:
            root.after(50, cmd)