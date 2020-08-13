# this script should be used with impacket
import psexec
ip = "10.10.10.10"
username=""
password=""
psobject = psexec.PSEXEC("cmd.exe", "c:\\windows\\system32\\", "445/SMB", username=username, password=password)
psobject.run(ip)
