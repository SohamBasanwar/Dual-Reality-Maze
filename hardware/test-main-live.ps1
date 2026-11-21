param([string]$Port='COM5')
# Bench check: leave the servo linkage free. All feedback requests closed (gate=0).
$serial=[System.IO.Ports.SerialPort]::new($Port,115200)
$serial.DtrEnable=$true
$serial.RtsEnable=$true
$serial.NewLine="`n"
$capture=''
try {
 $serial.Open()
 Start-Sleep -Milliseconds 500
 $capture+=$serial.ReadExisting()
 # Cross all warnings; repeat each command to check deduplication.
 $seconds=@(600,301,300,181,180,121,120,61,60,50,40,30,25,20,15,10,9,8,7,6,5,4,3,2,1,0)
 foreach($s in $seconds){
  $serial.WriteLine("S,0,1,$s")
  Start-Sleep -Milliseconds 150
  $capture+=$serial.ReadExisting()
  $serial.WriteLine("S,0,1,$s")
  Start-Sleep -Milliseconds 150
  $capture+=$serial.ReadExisting()
 }
 # An idle command and then silence must settle to green, not sticky red.
 $serial.WriteLine('S,0,0,0')
 Start-Sleep -Milliseconds 1800
 $capture+=$serial.ReadExisting()
} finally {if($serial.IsOpen){$serial.Close()};$serial.Dispose()}
$destination=Join-Path $PSScriptRoot 'verification/countdown-usb.jsonl'
$capture|Set-Content -LiteralPath $destination
$rows=@($capture -split "`n"|ForEach-Object{try{$v=$_|ConvertFrom-Json -ErrorAction Stop;if($null -ne $v){$v}}catch{}})
$rows|Select-Object -Last 1|ConvertTo-Json
[pscustomobject]@{Samples=$rows.Count;AnyBlue=@($rows|Where-Object led -eq blue).Count;AllExplorerOK=(@($rows|Where-Object eOK).Count -eq $rows.Count);AllArchitectOK=(@($rows|Where-Object aOK).Count -eq $rows.Count);WarningSeconds=@($rows|Where-Object beepSecond -gt 0|Select-Object -ExpandProperty beepSecond -Unique)}|ConvertTo-Json
