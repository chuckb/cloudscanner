#!/usr/bin/python

# Import libraries
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os

# This class adds a helper function to neatly send a message with an attachment.
# It requires a valid SMTP account, server, and port.

class MailUtil(object):
        def __init__(self, user = "", password = "", server = "", port = 587):
                self.user = user
		self.password = password
		self.server = server
		self.port = port

        @property
        def user(self):
                return self._user

        @user.setter
        def user(self, value):
                self._user = value

        @property
        def password(self):
                return self._password

        @password.setter
        def password(self, value):
                self._password = value

        @property
        def server(self):
                return self._server

        @server.setter
        def server(self, value):
                self._server = value

        @property
        def port(self):
                return self._port

        @port.setter
        def port(self, value):
                self._port = value

	def mail_with_attachment(self, to, subject, text, attach):
	   msg = MIMEMultipart()

	   msg['From'] = self.user 
	   msg['To'] = to
	   msg['Subject'] = subject

	   msg.attach(MIMEText(text))

	   part = MIMEBase('application', 'octet-stream')
	   part.set_payload(open(attach, 'rb').read())
	   Encoders.encode_base64(part)
	   part.add_header('Content-Disposition',
		   'attachment; filename="%s"' % os.path.basename(attach))
	   msg.attach(part)

	   mailServer = smtplib.SMTP(self.server, self.port)
	   mailServer.ehlo()
	   mailServer.starttls()
	   mailServer.ehlo()
	   mailServer.login(self.user, self.password)
	   mailServer.sendmail(self.user, to, msg.as_string())
	   # Should be mailServer.quit(), but that crashes...
	   mailServer.close()

