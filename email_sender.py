import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

server = smtplib.SMTP('smtp.gmail.com', 25)

server.starttls()

#server.connect("smtp.gmail.com", 465)

server.ehlo()

server.login('cs1813projectgroup1@gmail.com','Cs1813projectgroup1!')

def send_email(targetEmail, subject, message):
    msg = MIMEMultipart()
    msg['To'] = str(targetEmail)
    msg['Subject'] = str(subject)
    msg['From'] = "CS1813 Project Group"

    msg.attach(MIMEText(f"{message}\nWebsite: http://127.0.0.1:5000/", 'plain'))
    
    text = msg.as_string()

    server.sendmail('cs1813projectgroup1@gmail.com', str(targetEmail), text)
