#!/usr/bin/env python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body, to_email, from_email, smtp_server, smtp_port, smtp_user, smtp_password):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        print("SMTP user: {0}".format(smtp_user))
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection

        server.login(smtp_user, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("[+] Email sent successfully!")
    except Exception as e:
        print(f"[!] Failed to send email: {e}")

subject = "Required: Information is missing"
body = "Hello User, please update your information"
to_email = "send_to_user@email.com"
from_email = "your_email@email.com"
smtp_server = "smtp.server.com"
smtp_port = 587
smtp_user = from_email
smtp_password = "your_user_password"

send_email(subject, body, to_email, from_email, smtp_server, smtp_port, smtp_user, smtp_password)
