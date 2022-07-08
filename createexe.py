import glob

a = Analysis(['application.py'],
         pathex=['D:\\MyApplication'],
         binaries=[],
         datas=[],
         hiddenimports=[],
         hookspath=[],
         runtime_hooks=[],
         excludes=[],
         win_no_prefer_redirects=False,
         win_private_assemblies=False,
         cipher=block_cipher,
         noarchive=False)

a.datas += [("assets\\"+file.split("\\")[-1], file, "DATA") for file in glob.glob("D:\\MyApplication\\assets\\*")]

pyz = PYZ(a.pure, a.zipped_data,
         cipher=block_cipher)
exe = EXE(pyz,
      a.scripts,
      a.binaries,
      a.zipfiles,
      a.datas,
      [],
      name='MyApplication',
      debug=True,
      bootloader_ignore_signals=False,
      strip=False,
      upx=True,
      upx_exclude=[],
      runtime_tmpdir=None,
      console=True )

PyInstaller --noconsole --onefile --clean --add-data "assets/Logo_b.ico;."  --add-data "src/agentcount.py;." --add-data "src/browser.py;." --add-data "src/checkCases.py;." --add-data "src/clicky.py;." --add-data "src/config.py;." --add-data "src/constrants.py;." --add-data "src/end.py;." --add-data "src/selecty.py;." --add-data "src/setCases.py;." --add-data "src/setCommit.py;." --add-data "src/tabs.py;." --add-data "src/updatetk.py;." main.py


python3 -m PyInstaller --noconsole --onefile --icon=Logo_b.ico --add-data "Logo_b.ico;." main.py