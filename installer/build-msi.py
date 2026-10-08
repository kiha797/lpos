"""Run in this directory with wixl and msitools installed (Linux)."""
from pathlib import Path
import subprocess
import os
root=Path(__file__).resolve().parent
os.chdir(root)
output=root.parent/'dist'/'LabelPOS-Studio-Setup.msi'
subprocess.run(['wixl','-a','x64','-o',str(output),'LabelPOS.wxs'],check=True)
for name in ['Dialog','Control','ControlEvent','EventMapping','TextStyle','InstallUISequence','CustomAction','RemoveFile']:
 subprocess.run(['msibuild',str(output),'-i',name+'.idt'],check=True)
for query in ["INSERT INTO `InstallExecuteSequence` (`Action`, `Condition`, `Sequence`) VALUES ('StopLocalServer', 'REMOVE=\"ALL\"', 3490)","UPDATE `Property` SET `Value`='ErrorDlg' WHERE `Property`='ErrorDialog'","UPDATE `Property` SET `Value`='1033' WHERE `Property`='ProductLanguage'","UPDATE `Shortcut` SET `ShowCmd`=7"]:
 subprocess.run(['msibuild',str(output),'-q',query],check=True)
print(output)
