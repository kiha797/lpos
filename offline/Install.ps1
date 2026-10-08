$ErrorActionPreference='Stop'
$target=Join-Path $env:LOCALAPPDATA 'LabelPOS-Studio'
if ([IO.Path]::GetFullPath($PSScriptRoot) -eq [IO.Path]::GetFullPath($target)) { Write-Host 'Already installed. Run Start.cmd.'; exit }
if (Test-Path (Join-Path $target 'Stop.ps1')) { & (Join-Path $target 'Stop.ps1') }
New-Item -ItemType Directory -Path $target -Force | Out-Null
Get-ChildItem $PSScriptRoot | Where-Object {$_.Name -ne 'server.pid'} | ForEach-Object { Copy-Item $_.FullName $target -Recurse -Force }
$shell=New-Object -ComObject WScript.Shell
$paths=@([Environment]::GetFolderPath('Desktop'),(Join-Path ([Environment]::GetFolderPath('StartMenu')) 'Programs'))
foreach($path in $paths) {
 $shortcut=$shell.CreateShortcut((Join-Path $path 'LabelPOS Studio.lnk'));$shortcut.TargetPath=Join-Path $target 'Start.cmd';$shortcut.WorkingDirectory=$target;$shortcut.IconLocation=(Join-Path $target 'app\app.ico');$shortcut.WindowStyle=7;$shortcut.Save()
}
Write-Host 'Installed. Desktop shortcut: LabelPOS Studio'
Write-Host 'No administrator privileges or internet required.'
Start-Process (Join-Path $target 'Start.cmd')
