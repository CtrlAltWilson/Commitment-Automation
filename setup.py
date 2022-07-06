import sys,os
from cx_Freeze import setup, Executable
from src.constants import version

#TODO build exe

build_exe_options = {"path": sys.path}

setup(
    name = "Commitment Manager by Wilson",
    version = version,
    description='py.wilsonngo.com',
    executables = [Executable("main.py", icon="./assets/Logo.ico", targetName="CmtMgr.exe")],
    options={"build_exe": build_exe_options}
)