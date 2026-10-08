$ErrorActionPreference = 'Stop'
$port = 18763
$root = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot 'app'))
$listener = New-Object System.Net.Sockets.TcpListener([System.Net.IPAddress]::Loopback, $port)
function Open-Studio {
    $edge = @("${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe", "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe", "$env:LOCALAPPDATA\Microsoft\Edge\Application\msedge.exe") | Where-Object { Test-Path $_ } | Select-Object -First 1
    if ($edge) { Start-Process $edge -ArgumentList "--app=http://127.0.0.1:$port/" }
    else { Start-Process "http://127.0.0.1:$port/" }
}
try { $listener.Start() } catch {
    try { $test = Invoke-WebRequest "http://127.0.0.1:$port/health" -UseBasicParsing -TimeoutSec 3; if ($test.Content -eq 'LABELPOS-STUDIO-1') { Open-Studio; exit } } catch {}
    Write-Host 'Port 18763 is in use. Stop the previous LabelPOS session or contact support.'; Read-Host 'Press Enter'; exit 1
}
[IO.File]::WriteAllText((Join-Path $PSScriptRoot 'server.pid'), [string]$PID)
Open-Studio
Write-Host 'LabelPOS Studio offline server. Use Stop.cmd to stop.'
$mime = @{'.html'='text/html; charset=utf-8';'.js'='application/javascript; charset=utf-8';'.css'='text/css; charset=utf-8';'.svg'='image/svg+xml';'.png'='image/png';'.ico'='image/x-icon';'.json'='application/json';'.webmanifest'='application/manifest+json';'.zip'='application/zip'}
try {
 while ($true) {
  $client=$listener.AcceptTcpClient(); $client.ReceiveTimeout=2000; $client.SendTimeout=5000
  try {
   $stream=$client.GetStream(); $reader=New-Object IO.StreamReader($stream,[Text.Encoding]::ASCII,$false,1024,$true)
   $line=$reader.ReadLine(); if (!$line) { continue }; $parts=$line.Split(' ')
   $header=$reader.ReadLine(); while ($header) { $header=$reader.ReadLine() }
   if ($parts[0] -notin @('GET','HEAD')) { $status='405 Method Not Allowed'; $body=[Text.Encoding]::UTF8.GetBytes('Method not allowed'); $type='text/plain' }
   else {
    $path=[Uri]::UnescapeDataString(($parts[1].Split('?')[0])).TrimStart('/')
    if (!$path) { $path='index.html' }
    if ($path -eq 'health') { $status='200 OK'; $type='text/plain'; $body=[Text.Encoding]::ASCII.GetBytes('LABELPOS-STUDIO-1') }
    else {
     $file=[IO.Path]::GetFullPath((Join-Path $root $path.Replace('/',[IO.Path]::DirectorySeparatorChar)))
     if (!$file.StartsWith($root+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase) -or !(Test-Path $file -PathType Leaf)) { $status='404 Not Found';$type='text/plain';$body=[Text.Encoding]::UTF8.GetBytes('Not found') }
     else { $status='200 OK';$body=[IO.File]::ReadAllBytes($file);$ext=[IO.Path]::GetExtension($file);$type=$mime[$ext];if (!$type) {$type='application/octet-stream'} }
    }
   }
   $headers="HTTP/1.1 $status`r`nContent-Type: $type`r`nContent-Length: $($body.Length)`r`nCache-Control: no-cache`r`nX-Content-Type-Options: nosniff`r`nConnection: close`r`n`r`n"
   $bytes=[Text.Encoding]::ASCII.GetBytes($headers);$stream.Write($bytes,0,$bytes.Length)
   if ($parts[0] -ne 'HEAD') {$stream.Write($body,0,$body.Length)}
   $stream.Flush()
  } catch { } finally { $client.Close() }
 }
} finally { $listener.Stop(); Remove-Item (Join-Path $PSScriptRoot 'server.pid') -ErrorAction SilentlyContinue }
