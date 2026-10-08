$pidFile=Join-Path $PSScriptRoot 'server.pid'
if (Test-Path $pidFile) {
 $serverProcessId=0
 if ([int]::TryParse((Get-Content $pidFile -Raw).Trim(),[ref]$serverProcessId)) {
  $process=Get-CimInstance Win32_Process -Filter "ProcessId=$serverProcessId" -ErrorAction SilentlyContinue
  $serverPath=Join-Path $PSScriptRoot 'Server.ps1'
  if ($process -and $process.Name -eq 'powershell.exe' -and $process.CommandLine.Contains($serverPath)) { Stop-Process -Id $serverProcessId -ErrorAction SilentlyContinue }
 }
 Remove-Item $pidFile -ErrorAction SilentlyContinue
}
Write-Host 'LabelPOS server stopped. Saved designs are kept.'
