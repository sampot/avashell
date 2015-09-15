# -*- mode: python -*-
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys

app_name = 'avashell'
exe_name = 'avashell'
res_path = os.path.join('.', 'res')

if sys.platform == 'win32':
    exe_name = exe_name + '.exe'
    run_upx = False
    script = 'avashell/shell_win32.py'

elif sys.platform.startswith('linux'):
    run_strip = True
    run_upx = False
    script = 'avashell/shell_gtk.py'

elif sys.platform.startswith('darwin'):
    run_upx = False
    script = 'avashell/shell_osx.py'

else:
    print("Unsupported operating system")
    sys.exit(-1)


# for copying data file according to PyInstaller's recipe
def Datafiles(*filenames, **kw):
    import os

    def datafile(path, strip_path=True):
        parts = path.split('/')
        path = name = os.path.join(*parts)
        if strip_path:
            name = os.path.basename(path)
        return name, path, 'DATA'

    strip_path = kw.get('strip_path', True)
    return TOC(
        datafile(filename, strip_path=strip_path)
        for filename in filenames
        if os.path.isfile(filename))

# declared the extra script files to be added
shfiles = Datafiles('avaconfig.py', 'avastartup.py')


a = Analysis([script],
             pathex=[],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)

pyz = PYZ(a.pure)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name=exe_name,
          debug=False,
          strip=None,
          upx=True,
          icon= os.path.join(res_path, 'icon.ico'),
          console=False)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               Tree(res_path, 'res', excludes=['*.pyc']),
               a.datas,
               shfiles,          # add script files to the collection.
               strip=None,
               upx=run_upx,
               name=app_name)

if sys.platform.startswith('darwin'):
    app = BUNDLE(coll,
                name='Avashell.app',
                appname=exe_name,
                icon=os.path.join(res_path, 'icon.icns'))