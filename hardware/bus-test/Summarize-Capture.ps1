param([string]$FileName='nov10-recheck.txt')
$rows=@(Get-Content -LiteralPath (Join-Path $PSScriptRoot $FileName) | ForEach-Object {try{$_ | ConvertFrom-Json -ErrorAction Stop}catch{}})
$result=[ordered]@{capture=$FileName;status=($rows | Where-Object type | Select-Object -Last 1);boards=@()}
foreach($g in ($rows | Where-Object addr | Group-Object addr)){
 $valid=@($g.Group | Where-Object valid)
 $good=@($g.Group | Where-Object {$_.valid -and $_.echoOK -and $_.tx -eq 0})
 $result.boards+=[ordered]@{
  address=[int]$g.Name; samples=$g.Count; valid=$valid.Count; successfulExchanges=$good.Count
  failures=($g.Count-$good.Count); xMin=($valid.x|Measure-Object -Minimum).Minimum;xMax=($valid.x|Measure-Object -Maximum).Maximum
  yMin=($valid.y|Measure-Object -Minimum).Minimum;yMax=($valid.y|Measure-Object -Maximum).Maximum
  pressedSamples=@($valid|Where-Object button).Count;pressCounterMax=($valid.presses|Measure-Object -Maximum).Maximum
  firstMS=$g.Group[0].ms;lastMS=$g.Group[-1].ms
 }
}
$result | ConvertTo-Json -Depth 6
