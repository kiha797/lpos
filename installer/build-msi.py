"""Build the per-user MSI with validated short|long filename metadata."""
from pathlib import Path
import subprocess,os,re
root=Path(__file__).resolve().parent
os.chdir(root)
output=root.parent/'dist'/'LabelPOS-Studio-Setup.msi'
wixl=os.environ.get('WIXL_BIN','wixl')
msibuild=os.environ.get('MSIBUILD_BIN','msibuild')
msiinfo=os.environ.get('MSIINFO_BIN','msiinfo')
def query(sql):subprocess.run([msibuild,str(output),'-q',sql],check=True)
def rows(table):
 text=subprocess.check_output([msiinfo,'export',str(output),table]).decode()
 lines=text.splitlines();cols=lines[0].split('\t')
 return [dict(zip(cols,line.split('\t'))) for line in lines[3:] if line]
def quote(s):return "'"+s.replace("'","''")+"'"
def short_ok(s):return bool(re.fullmatch(r'[A-Za-z0-9_~!#$%&()@^{}-]{1,8}(\.[A-Za-z0-9_~!#$%&()@^{}-]{1,3})?',s))
def aliases(records,key,name,group):
 used={}
 for r in records:
  g=group(r);used.setdefault(g,set())
  n=r[name].split('|')[0]
  if short_ok(n):used[g].add(n.upper())
 for r in records:
  n=r[name]
  if n=='.' or '|' in n or short_ok(n):continue
  g=group(r);stem,sep,ext=n.rpartition('.')
  if not sep:stem,ext=n,''
  clean=re.sub('[^A-Za-z0-9]','',stem).upper() or 'LPFILE'
  ext=re.sub('[^A-Za-z0-9]','',ext).upper()[:3]
  i=1
  while True:
   tail='~'+str(i);alias=clean[:8-len(tail)]+tail+('.'+ext if ext else '')
   if alias not in used[g]:break
   i+=1
  used[g].add(alias);r[name]=alias+'|'+n
 return records
subprocess.run([wixl,'-a','x64','-o',str(output),'LabelPOS.wxs'],check=True)
for name in ['Dialog','Control','ControlEvent','EventMapping','TextStyle','InstallUISequence','CustomAction','RemoveFile']:
 subprocess.run([msibuild,str(output),'-i',name+'.idt'],check=True)
for sql in ["INSERT INTO `InstallExecuteSequence` (`Action`, `Condition`, `Sequence`) VALUES ('StopLocalServer', 'REMOVE=\"ALL\"', 3490)","UPDATE `Property` SET `Value`='ErrorDlg' WHERE `Property`='ErrorDialog'","UPDATE `Property` SET `Value`='1033' WHERE `Property`='ProductLanguage'","UPDATE `Shortcut` SET `ShowCmd`=7","INSERT INTO `Property` (`Property`, `Value`) VALUES ('MsiLogging', 'voicewarmupx')"]:query(sql)
components={r['Component']:r['Directory_'] for r in rows('Component')}
for table,key,name,group in [('File','File','FileName',lambda r:components[r['Component_']]),('Directory','Directory','DefaultDir',lambda r:r['Directory_Parent']),('Shortcut','Shortcut','Name',lambda r:r['Directory_'])]:
 records=rows(table)
 if table=='Directory':records=[r for r in records if r['Directory']!='TARGETDIR']
 for r in aliases(records,key,name,group):
  if '|' in r[name]:query('UPDATE `'+table+'` SET `'+name+'`='+quote(r[name])+' WHERE `'+key+'`='+quote(r[key]))
# Check the exact MSI metadata, not only the XML source.
for table,col in [('File','FileName'),('Directory','DefaultDir'),('Shortcut','Name')]:
 for r in rows(table):
  if table=='Directory' and (r['Directory']=='TARGETDIR' or r[col]=='.'):continue
  if not short_ok(r[col].split('|')[0]):raise ValueError('Invalid 8.3 filename: '+r[col])
subprocess.run([os.sys.executable,str(root/'verify-msi.py'),str(output)],check=True)
print(output)
