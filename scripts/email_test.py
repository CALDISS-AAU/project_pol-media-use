import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

msg = MIMEMultipart()
    
msg['From'] = 'kristian@mail.bot'
msg['To'] = 'kgk@adm.aau.dk'
msg['Subject'] = "I can send e-mail?"

s = smtplib.SMTP('smtp-relay.sendinblue.com', 587)
s.starttls()
s.login("kgk@adm.aau.dk", "a94Q187jgzb0vWEO")

message = "<p><i>I want e-mail</i></p>"
msg.attach(MIMEText(message, 'html'))

s.send_message(msg)   