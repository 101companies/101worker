import csv
import string
import smtplib
from email.mime.text import MIMEText

# Configure addresses and server
emailFrom = "softlang@uni-koblenz.de"
emailTo = "dotnetby@gmail.com" # for testing
#emailTo = "gatekeepers@101companies.org"
emailServer = "deliver.uni-koblenz.de"

def buildMailContent():
	logfile = open('../101logs/runner.log', 'r')
	lastArchive = open('../101web/logs/lastArchive', 'r')
	time = lastArchive.read()
	log = csv.reader(open('../101logs/runner.log', 'r'), delimiter=';', quotechar='|')
	for row in log[1::]:
		print ', '.join(row)+";"+"http://data.101companies.org/logs/"+time+row[0]+".log"
	return log

# Send the email
if (string.find(buildMailContent(), 'FAIL')>=0):
	msg = MIMEText(log.encode('utf-8'), 'plain', 'utf-8')
	msg["To"] = emailTo
	msg["From"] = emailFrom
	msg["Subject"] = "[101worker] 101logs/runner.log"
	smtp = smtplib.SMTP()
	smtp.connect(emailServer)
	smtp.sendmail(emailFrom, msg["To"], msg.as_string())
