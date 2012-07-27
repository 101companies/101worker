import csv
import string
import smtplib
from email.mime.text import MIMEText

from mailer import Mailer
from mailer import Message

# Configure addresses and server
emailFrom = "softlang@uni-koblenz.de"
#emailTo = "dotnetby@gmail.com" # for testing
emailTo = "gatekeepers@101companies.org"
emailServer = "deliver.uni-koblenz.de"

tmpl = "<table><tr><td>Status</td><td>Module</td></tr>"
tmpl_end = "</table>"

def buildMailContent():
	logfile = open('../101logs/runner.log', 'r')
	lastArchive = open('../101web/logs/lastArchive', 'r')
	time = lastArchive.read()
	log = csv.reader(open('../101logs/runner.log', 'r'), delimiter=';', quotechar='|')
	content = tmpl
	for row in log:
		if len(row) > 2:
			l = "<tr><td>"+row[3]+"</td><td><a href='http://data.101companies.org/logs/"+time+"/"+row[0]+".log'>"+row[0]+"</a></td></tr>"
			#print l
			content += l
	content += tmpl_end		
	return content

# Send the email
log = buildMailContent()
if (string.find(log, 'FAIL')>=0):
	#msg = MIMEText(log.encode('utf-8'), 'text/html', 'utf-8')
	#msg["To"] = emailTo
	#msg["From"] = emailFrom
	#msg["Subject"] = "[101worker] 101logs/runner.log"
	#smtp = smtplib.SMTP()
	#smtp.connect(emailServer)
	#smtp.sendmail(emailFrom, msg["To"], msg.as_string())

	message = Message(From=emailFrom,To=emailTo)
	message.Subject = "[101worker] Execution Status Report"
	message.Html = log
	sender = Mailer(emailServer)
	sender.send(message)
