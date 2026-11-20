$rows=@(Get-Content (Join-Path $PSScriptRoot 'wifi-live.jsonl') | ForEach-Object {try{$_|ConvertFrom-Json -ErrorAction Stop}catch{}})
$data=@($rows|Where-Object diagnostic)
$e=@($data.boards|Where-Object {$_.addr -eq 17 -and $_.valid -and $_.echoOK -and $_.tx -eq 0})
$a=@($data.boards|Where-Object {$_.addr -eq 16 -and $_.valid -and $_.echoOK -and $_.tx -eq 0})
$motion=@($a|Where-Object {$_.servoUs -gt 0})
$result=[ordered]@{
 created=(Get-Date).ToString('o');httpResponses=$data.Count;httpErrors=@($rows|Where-Object error).Count
 invalidBoardSamples=@($data.boards|Where-Object {-not $_.valid -or -not $_.echoOK -or $_.tx -ne 0}).Count
 joystick=[ordered]@{xMin=($e.x|Measure-Object -Minimum).Minimum;xMax=($e.x|Measure-Object -Maximum).Maximum;yMin=($e.y|Measure-Object -Minimum).Minimum;yMax=($e.y|Measure-Object -Maximum).Maximum;startPresses=$e[0].presses;lastPresses=$e[-1].presses;finalX=$e[-1].x;finalY=$e[-1].y;pressedSamples=@($e|Where-Object button).Count}
 servo=[ordered]@{reportedPulseSamples=$motion.Count;sampledPulseMin=($motion.servoUs|Measure-Object -Minimum).Minimum;sampledPulseMax=($motion.servoUs|Measure-Object -Maximum).Maximum;finalPulseUs=$a[-1].servoUs;commandAcknowledgments=@($rows|Where-Object commandSent|Select-Object path,receivedAt,tx)}
}
$result|ConvertTo-Json -Depth 7|Set-Content (Join-Path $PSScriptRoot 'RESULTS.json') -Encoding utf8
$result|ConvertTo-Json -Depth 7
