param([int]$Seconds=45,[string]$OutputName='joystick-serial.txt',[string]$Command='')
$port=[System.IO.Ports.SerialPort]::new('COM5',115200)
$port.DtrEnable=$true
$port.ReadTimeout=500
$buffer=''
try {
 $port.Open()
 if($Command){Start-Sleep -Milliseconds 1500;$port.Write($Command)}
 Write-Output 'Capture started on Main COM5.'
 $timer=[Diagnostics.Stopwatch]::StartNew()
 while($timer.Elapsed.TotalSeconds -lt $Seconds){$buffer+=$port.ReadExisting();Start-Sleep -Milliseconds 50}
} finally {if($port.IsOpen){$port.Close()};$port.Dispose()}
$buffer | Set-Content -LiteralPath (Join-Path $PSScriptRoot $OutputName) -Encoding utf8
$rows=@($buffer -split "`n" | ForEach-Object {try{$_ | ConvertFrom-Json -ErrorAction Stop}catch{}})
foreach($g in ($rows | Group-Object addr)){
 [pscustomobject]@{Address=$g.Name;Samples=$g.Count;Valid=(@($g.Group | Where-Object valid)).Count;EchoOK=(@($g.Group | Where-Object echoOK)).Count;XMin=($g.Group.x | Measure-Object -Minimum).Minimum;XMax=($g.Group.x | Measure-Object -Maximum).Maximum;YMin=($g.Group.y | Measure-Object -Minimum).Minimum;YMax=($g.Group.y | Measure-Object -Maximum).Maximum;ButtonPressedSamples=(@($g.Group | Where-Object button)).Count} | ConvertTo-Json -Compress
}
