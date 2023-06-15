import smtplib, ssl
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date

class Email:
    def __init__(self):
        self.port = 465  # For SSL
        self.password = os.environ['EMAIL_PASSWORD']
        self.email = os.environ['EMAIL_ADDRESS']

    def send(self, destination, subject, recomendation):
        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", self.port, context=context) as server:
            server.login(self.email, self.password)
            server.sendmail(self.email, destination, self.meessage(self.email, destination, subject, recomendation).as_string())
            server.quit()

    def meessage(self, from_email, to_email, subject, recomendation):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email
        today = date.today()

        # Create the body of the message (a plain-text and an HTML version).
        styles = """
            body { color: #666; }
            p { color: #333; font-size: 2rem; text-align: center; text-transform: uppercase; }
        """
        text = ""
        html = """\
        <html>
          <head>
            <style>
                {}
            </style>
          </head>
          <body style="color: #666">
            <h2>Daily recomendation</h2>
            <div>Date: {}</div>
            <p style="font-size: 1.2rem; border: solid 2px #999; border-radius: 5px; backgroud-color: #ddd; padding: 1rem 2rem; ">
                Recomendation: <span style="text-transform: capitalize; color: #242">{}</span>
            </p>
            <h3 style="color: #898">By SMA Team</h3>
          </body>
        </html>
        """.format(styles, today.strftime("%d/%m/%Y"), recomendation)

        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        msg.attach(part1)
        msg.attach(part2)
        return msg
