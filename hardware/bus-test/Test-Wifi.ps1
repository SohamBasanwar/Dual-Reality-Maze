$ErrorActionPreference='Stop'
$oldProfile=(Get-NetConnectionProfile | Where-Object InterfaceAlias -eq 'Wi-Fi' | Select-Object -First 1).Name
$xml=@"
<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
<name>DualRealityMaze</name><SSIDConfig><SSID><name>DualRealityMaze</name></SSID></SSIDConfig>
<connectionType>ESS</connectionType><connectionMode>manual</connectionMode>
<MSM><security><authEncryption><authentication>WPA2PSK</authentication><encryption>AES</encryption><useOneX>false</useOneX></authEncryption>
<sharedKey><keyType>passPhrase</keyType><protected>false</protected><keyMaterial>MazeDemo362</keyMaterial></sharedKey>
</security></MSM></WLANProfile>
"@
$profilePath=Join-Path $PSScriptRoot 'diagnostic-wifi-profile.xml'
$xml | Set-Content -LiteralPath $profilePath -Encoding utf8
try {
 netsh wlan add profile filename="$profilePath" user=current
 netsh wlan connect name=DualRealityMaze ssid=DualRealityMaze interface="Wi-Fi"
 Start-Sleep -Seconds 8
 $samples=@()
 for($i=0;$i -lt 5;$i++){
  try {
   $r=Invoke-RestMethod -Uri 'http://192.168.4.1/' -TimeoutSec 4 -Proxy $null
   $samples+=$r
   $r | ConvertTo-Json -Depth 6 -Compress
  } catch { Write-Output $_.Exception.Message }
  Start-Sleep -Seconds 1
 }
 $samples | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'nov10-wifi-http.json') -Encoding utf8
} finally {
 if($oldProfile){netsh wlan connect name="$oldProfile" interface="Wi-Fi" | Out-Null; Write-Output 'Restored previous Wi-Fi connection request.'}
}
