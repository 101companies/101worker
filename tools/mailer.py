import csv
import string
import smtplib
from email.mime.text import MIMEText

# Configure addresses and server
emailFrom = "softlang@uni-koblenz.de"
emailTo = "dotnetby@gmail.com" # for testing
#emailTo = "gatekeepers@101companies.org"
emailServer = "deliver.uni-koblenz.de"

tmpl = "<!DOCTYPE html><html><body><table><tr><td>Module</td><td>Status</td><td>Log</td></tr>"
tmpl_end = "</table></body></html>"

def buildMailContent():
	logfile = open('../101logs/runner.log', 'r')
	lastArchive = open('../101web/logs/lastArchive', 'r')
	time = lastArchive.read()
	log = csv.reader(open('../101logs/runner.log', 'r'), delimiter=';', quotechar='|')
	content = tmpl
	for row in log:
		if len(row) > 2:
			l = "<tr><td>"+row[0]+"</td><td>"+row[3]+"</td><td>http://data.101companies.org/logs/"+time+"/"+row[0]+".log</td></tr>"
			#print l
			content += l
	content += tmpl_end		
	return content

# Send the email
log = buildMailContent()
if (string.find(log, 'FAIL')>=0):
	msg = MIMEText(log.encode('utf-8'), 'text/html', 'utf-8')
	msg["To"] = emailTo
	msg["From"] = emailFrom
	msg["Subject"] = "[101worker] 101logs/runner.log"
	smtp = smtplib.SMTP()
	smtp.connect(emailServer)
	smtp.sendmail(emailFrom, msg["To"], msg.as_string())
