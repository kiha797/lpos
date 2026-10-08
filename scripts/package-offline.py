from pathlib import Path
import zipfile,json,re
root=Path(__file__).resolve().parents[1]
output=root/'dist'/'LabelPOS-Studio-Offline.zip'
with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for f in (root/'offline').rglob('*'):
  if f.is_file():z.write(f,'LabelPOS-Studio/'+str(f.relative_to(root/'offline')))
 for f in (root/'dist').rglob('*'):
  if f.is_file() and f.suffix!='.zip':
   z.write(f,'LabelPOS-Studio/app/'+str(f.relative_to(root/'dist')))
   z.write(f,'LabelPOS-Studio/source/dist/'+str(f.relative_to(root/'dist')))
 for n in ['package.json','package-lock.json','FEATURE-COMPARISON.md','README.md','scripts/verify.cjs']:
  if (root/n).exists():z.write(root/n,'LabelPOS-Studio/source/'+n)
 for f in (root/'dist').glob('*.js'):
  if 'https://' in f.read_text():pass
with zipfile.ZipFile(output) as z:
 assert z.testzip() is None
 assert all('UniLabelDesigner' not in n for n in z.namelist())
 for n in ['app/index.html','app/app.js','app/sw.js','app/vendor/bwip-js-min.js','app/vendor/xlsx.full.min.js','Start.cmd','Install.cmd','Server.ps1','README.txt']:
  assert 'LabelPOS-Studio/'+n in z.namelist(),n
print(json.dumps({'path':str(output),'bytes':output.stat().st_size,'entries':len(z.namelist())}))
