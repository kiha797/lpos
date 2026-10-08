$ErrorActionPreference='Stop'
& (Join-Path $PSScriptRoot 'Stop.ps1')
foreach($path in @([Environment]::GetFolderPath('Desktop'),(Join-Path ([Environment]::GetFolderPath('StartMenu')) 'Programs'))) { Remove-Item (Join-Path $path 'LabelPOS Studio.lnk') -ErrorAction SilentlyContinue }
$target=Join-Path $env:LOCALAPPDATA 'LabelPOS-Studio'
if ([IO.Path]::GetFullPath($PSScriptRoot) -eq [IO.Path]::GetFullPath($target)) { Remove-Item $target -Recurse -Force }
Write-Host 'Uninstalled. Browser-local design data is retained. Back up important .lpos files.'
