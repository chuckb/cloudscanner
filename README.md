cloudscanner
============

Turn your Raspberry Pi into a scan adapter to easily send PDFs to the cloud.

The complete project can be found at my blog, with all necessary dependencies and complete install instructions.

Once you have done that, pull these files into a directory on the Pi.

Edit the scanmail.py file and change the following constants:

GMAIL_USER = "put your gmail address here"

GMAIL_PASSWORD = "put your gmail password here"

SMTP_SERVER = "smtp.gmail.com"

...
destinations.append(EmailScanDestination("mail name to display on Pi", "mail destination address goes here"))

To start it:

./python scanmain.py &

Enjoy!
