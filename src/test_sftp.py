import pysftp
import sys

# Defines the name of the file for download / upload
FTP_ADDRESS="000kwjq.wcomhost.com"
FTP_USER_ID="ftp3286307"
password = sys.argv[1]

cnopts = pysftp.CnOpts(knownhosts='path/to/your/knownhostsfile')
cnopts.hostkeys = None

srv = pysftp.Connection(host=FTP_ADDRESS, username=FTP_USER_ID, password=password, cnopts=cnopts)

print(dir(srv))

# Closes the connection
srv.close()