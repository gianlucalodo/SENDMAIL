#!/usr/bin/python

import sys
import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import Encoders

#temporary path used to send attachments
tmppath='/tmp/'

#hostname/IP SMTP server
host='examplehostname'

#From
SEND_FROM = 'from@example.com'

class Email:
    def send(self, send_from, send_to, send_cc, send_bcc, subject, body, files=[]):
        COMMASPACE = ', '
        msg = MIMEMultipart('related')
        msg['Subject'] = subject
        msg['From'] = send_from
        msg['To'] = COMMASPACE.join(send_to)
        msg['Cc'] = COMMASPACE.join(send_cc)
        msg['Bcc'] = COMMASPACE.join(send_bcc)
        html = body
        part1 = MIMEText(html, 'html')
        msg.attach(part1)
        if(len(files) != 0):
            for f in files:
                part2 = MIMEBase('application', "octet-stream")
                part2.set_payload(open(tmppath + f, "rb").read())
                Encoders.encode_base64(part2)
                part2.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
                msg.attach(part2)
                print "Attached file: %s" % f
                os.remove(tmppath + f)
        s = smtplib.SMTP(host)
        s.sendmail(send_from, send_to+send_cc+send_bcc, msg.as_string())
        s.quit()
        print " --> Mail sent."


if __name__ == "__main__":
    if(len(sys.argv) < 6):
        print "Arguments not properly set!!!"
        sys.exit(0)
    RECIPIENT = (sys.argv[1]).split('|')
    CC_RECIPIENT = (sys.argv[2]).split('|')
    BCC_RECIPIENT = (sys.argv[3]).split('|')
    OBJECT = str(sys.argv[4])
    BODY_ORIG = str(sys.argv[5]).replace("\\n", "<br>")
    BODY = "<html><pre>%s</pre></html>" % BODY_ORIG
    ATTACHMENT = []
    if(len(sys.argv) >= 7):
        ATTACHMENT = sys.argv[6:]
    new_mail = Email()
    new_mail.send(SEND_FROM, RECIPIENT, CC_RECIPIENT, BCC_RECIPIENT, OBJECT, BODY, ATTACHMENT)
    sys.exit(1)
