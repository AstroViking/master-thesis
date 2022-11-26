#!/usr/bin/python

from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile
import os
from pathlib import Path
import subprocess

latex_package_path = Path('./latex_packages')

latex_home_path = Path(input('Enter the path where your LaTeX installation binaries (tlmgr, updmap-sys) reside: '))
tlmgr_path = latex_home_path / 'tlmgr'
mktexlsr_path = latex_home_path / 'mktexlsr'
updmap_sys_path = latex_home_path / 'updmap-sys'

if not tlmgr_path.exists():
    print(f"tlmgr does not exist at: {tlmgr_path}")
    exit(1)

if not mktexlsr_path.exists():
    print(f"umktexlsr does not exist at: {mktexlsr_path}")
    exit(1)

if not updmap_sys_path.exists():
    print(f"updmap-sys does not exist at: {updmap_sys_path}")
    exit(1)


# Download and unzip package
http_response = urlopen('https://mirrors.ctan.org/fonts/mtp2lite.zip')
zipfile = ZipFile(BytesIO(http_response.read()))
zipfile.extractall(path=latex_package_path)

# Install local latex package
#subprocess.run([tlmgr_path, 'conf', 'auxtrees', 'add', (latex_package_path / "mtp2lite" / "texmf").absolute()])
subprocess.run([mktexlsr_path])
subprocess.run([updmap_sys_path, '--enable', 'Map', 'mtpro2.map'])