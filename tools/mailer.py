import string
import smtplib
from email.mime.text import MIMEText

# Configure addresses and server
emailFrom = "softlang@uni-koblenz.de"
emailTo = "dotnetby@gmail.com" # for testing
#emailTo = "gatekeepers@101companies.org"
emailServer = "deliver.uni-koblenz.de"

# Send the email
logfile = open('../101logs/runner.log', 'r')
log = logfile.read()
if (string.find(log, 'FAIL (')>=0):
	msg = MIMEText(log.encode('utf-8'), 'plain', 'utf-8')
	msg["To"] = emailTo
	msg["From"] = emailFrom
	msg["Subject"] = "[101worker] 101logs/runner.log"
	smtp = smtplib.SMTP()
	smtp.connect(emailServer)
	smtp.sendmail(emailFrom, msg["To"], msg.as_string())
