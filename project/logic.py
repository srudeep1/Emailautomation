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
    send_message(s)

def send_message(smtobject):
    with open('config/message.yml') as f:
        data=yaml.load(f, Loader=yaml.FullLoader)
    for i in data:
        From,Toname,Subject,Message=fetch_message_details(data,i)
        validate=validate_contacts(Toname)
        if validate is not True:
            exit()
        condetails=fetch_contact_details(Toname)
        for i in condetails:
           key=list(i.keys())[0]
           value=i.get('{}'.format(key))
           tempmessage=Message.format(key)
           msg=message(From,value,Subject,tempmessage)
           smtobject.send_message(msg)

def validate_contacts(Toname):
    contactnames=[]
    with open('contacts/contacts.yml') as f:
       contacts=yaml.load(f, Loader=yaml.FullLoader)
    for j in contacts['contacts']:
       key=list(j.keys())[0]
       contactnames.append(key)
    print (contactnames)
    for i in Toname:
       if i not in contactnames:
          msg="The user {} is not found in contacts/contacts.yml. " \
               "Please Enter correct user name in config/message.yml " \
              "and re-run".format(i)
          return msg
       else:
          continue
    return True

def fetch_contact_details(Toname):
    condetails=[]
    with open('contacts/contacts.yml') as f:
        contacts=yaml.load(f, Loader=yaml.FullLoader)
    for i in Toname:
        for j in contacts['contacts']:
            if i in j:
               condetails.append(j)
    return condetails

def fetch_message_details(data,j):
    for i in data['{}'.format(j)]:
       if 'FROM' in i:
           From=i['FROM']
       if 'TONAME' in i:
           To=i['TONAME']
           To=To.split(',')
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


