# import the smtplib module. It should be included in Python by default
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import yaml

def create_smtplib(hostname,portno):
    smt = smtplib.SMTP(host= hostname, port=portno)
    return smt

def run():
    s=create_smtplib('smtp.gmail.com',587)
    s.ehlo()
    s.starttls()
    s.login("srudeep.9@gmail.com","qltzilpmbfjgqctb")
    From,To,Subject,Message=fetch_message_details()
    msg=message(From,To,Subject,Message)
    s.send_message(msg)

def fetch_message_details():
    with open('config/message.yml') as f:
        data=yaml.load(f, Loader=yaml.FullLoader)
    for i in data['data']:
       if 'FROM' in i:
           From=i['FROM']
       if 'TO' in i:
           To=i['TO']
       if 'SUBJECT' in i:
           Subject=i['SUBJECT']
       if 'MESSAGE' in i:
           Message=i['MESSAGE']
    return From,To,Subject,Message


def message(From,To,Subject,Message):
    msg = MIMEMultipart()
    msg['From']=From
    msg['To']=To
    msg['Subject']=Subject
    message=Message
    msg.attach(MIMEText(message,'plain'))
    return msg

if __name__ == "__main__":
    run()


