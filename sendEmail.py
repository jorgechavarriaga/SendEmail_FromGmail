import smtplib, os, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

SMTPSERVER = os.environ.get('SMTPSERVER')
SMTPPORT = os.environ.get('SMTPPORT')
EMAILFROM = os.environ.get('EMAILFROM')
PASSWORD = os.environ.get('PASSWORD')
EMAILTO = os.environ.get('EMAILTO')
EMAILCC = os.environ.get('EMAILCC')
EMAILBCC = os.environ.get('EMAILBCC')
email_address_supplied = True

def sendEmail(subject, content, emailto="", emailcc="", emailbcc=""):
    if emailto or emailcc or emailbcc:
        email_address_supplied = True
    else:
        email_address_supplied = False
    if email_address_supplied:
        htmlContect = []
        try:
            dateNow = datetime.datetime.now().strftime("%c")
            email_message = MIMEMultipart()
            email_message['From'] = EMAILFROM
            email_message['Subject'] = f'{subject} - {dateNow} '
            for data in content:
                # htmlContect.append(f'[-] {data} <br>')
                htmlContect.append(f'<ul><li>{data}</li></ul>')
            for line in htmlContect:
                email_message.attach(MIMEText(line, "html"))
            email_string = email_message.as_string()
            with smtplib.SMTP_SSL(SMTPSERVER, SMTPPORT) as server:
                server.login(EMAILFROM, PASSWORD)
                server.sendmail(EMAILFROM, [ emailto, emailcc, emailbcc], email_string)
            timeTry= datetime.datetime.now().strftime('%c')
            msg = f'[+] {timeTry} - Mail sent successfully.\n'
            print(msg)
            with open('sendEmailLog.log', "a") as f:
                f.write(msg)
        except Exception as e:
            timeExcept= datetime.datetime.now().strftime('%c')
            msg = f'[-] {timeExcept} - The email could not be sent.\n[-] {timeExcept} - ERROR: {e}'
            print(msg)
            with open('sendEmailLog.log', "a") as f:
                f.write(msg)
    else:
        print("[-] Missing email address, please supply an emailto or emailcc or emailbcc")


content = "Hi My Name is ...."
sendEmail("Test ", content, "jorge.chavarriaga@gmail.com")