#!/usr/bin/python

import platform
import os
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile
from pathlib import Path
import subprocess


operating_system = platform.system()

if(operating_system == 'Windows'):
    tinytex_binary_path = Path(f'{os.getenv("APPDATA")}/TinyTeX/bin/win32').absolute()
elif(operating_system == 'Darwin'):
    tinytex_binary_path = Path('~/Library/TinyTex/bin/universal-darwin').expanduser().absolute()
elif(operating_system == 'Linux'):
    tinytex_binary_path = Path('~/.TinyTeX/bin/').expanduser().absolute()
else:
    print(f'Operating system "{operating_system}" unknown!')
    exit(1)

latex_package_path = Path('./latex_packages').absolute()

tlmgr_path = tinytex_binary_path / 'tlmgr'
mktexlsr_path = tinytex_binary_path / 'mktexlsr'
kpsewhich_path = tinytex_binary_path / 'kpsewhich'
updmap_sys_path = tinytex_binary_path / 'updmap-sys'

if not tlmgr_path.exists():
    print(f"tlmgr does not exist at: {tlmgr_path}")
    exit(1)

if not kpsewhich_path.exists():
    print(f"kpsewhich does not exist at: {kpsewhich_path}")
    exit(1)

if not mktexlsr_path.exists():
    print(f"mktexlsr does not exist at: {mktexlsr_path}")
    exit(1)

if not updmap_sys_path.exists():
    print(f"updmap-sys does not exist at: {updmap_sys_path}")
    exit(1)

result = subprocess.run([kpsewhich_path, 'mtpro2.sty'])

if result.returncode == 0:
    print('MathTime Professional 2 Fonts are already installed.')
    exit(0)

# Download and unzip package
http_response = urlopen('https://mirrors.ctan.org/fonts/mtp2lite.zip')
zipfile = ZipFile(BytesIO(http_response.read()))
zipfile.extractall(path=latex_package_path)

# Install local latex package
subprocess.run([tlmgr_path, 'conf', 'auxtrees', 'add', (latex_package_path / "mtp2lite" / "texmf").absolute()])
subprocess.run([mktexlsr_path])
subprocess.run([updmap_sys_path, '--enable', 'Map', 'mtpro2.map'])