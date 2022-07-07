from PyInstaller import *

#will come back one day
added_files = [
        ( 'assets', '.' ),
        ( 'src/*', '.' )
        ]
a = Analysis(
        datas = added_files
        )