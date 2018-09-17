#!/usr/bin/env python3

import smtplib
import email
import sys
import getpass
import argparse
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate

yahoo_smtp_server                = 'smtp.mail.yahoo.com' # replace with required smtp server

def sendattachment(subject, send_from, send_to, password, \
                    file, server):

    try:
        msg                         = MIMEMultipart()
        msg['From']                = send_from
        msg['To']                = send_to
        msg['Date']                = formatdate(localtime=True)
        msg['Subject']        = subject

        with open(file, 'rb') as fp:
            part = MIMEApplication(fp.read(), Name=basename(file))

        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file)
        msg.attach(part)

        try:
            smtp = smtplib.SMTP(server, 587) # replace with smtp server port
            smtp.ehlo()
            smtp.starttls()
            smtp.login(send_from, password)
        except:
            print('[!] There Was A Problem Logging In To Email Server. Double Check Credentials and Allow Less Secure Apps')
            sys.exit(1)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.close()

    except:
        print('[!] You had been logged out! Sign in again later!')
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Send Attachment To Email")
    parser.add_argument('-f', '--file', type=str, required=True, metavar='',\
                        help='File To Attach')
    parser.add_argument('-u', '--username', type=str, required=True, metavar='',\
                        help='Your Email')
    parser.add_argument('-r', '--receiver', type=str, required=True, metavar='',\
                        help='Receiver Email')
    parser.add_argument('-s', '--subject', type=str, required=True, metavar='',\
                        help='Subject')

    args = parser.parse_args()
    
    password = getpass.getpass()
    username = args.username
    file = args.file
    receiver = args.receiver
    subject = args.subject

    sendattachment(subject, username, receiver, password, file, yahoo_smtp_server)
    print('\n[+] Sent: "{}" with attachment: "{}" to {}\n'.format(subject, basename(file), receiver))

if __name__ == '__main__':
    main()
    
