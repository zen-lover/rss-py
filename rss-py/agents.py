import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailAgent:

    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.smtp = smtplib.SMTP(host, port)
        self.smtp.starttls()
        self.smtp.login(username, password)

    def send(self, from_, to, subject, body):
        # Create a message
        message = MIMEMultipart()

        # Setup the parameters of the message
        message['From'] = from_
        message['To'] = to
        message['Subject'] = subject

        # Add in the message body
        message.attach(MIMEText(body, 'plain'))

        # Sendding the message
        self.smtp.send_message(message)
        self.smtp.quit()