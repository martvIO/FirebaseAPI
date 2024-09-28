import os
from pathlib import Path
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib

email = "martv2360@gmail.com"
email_receiver = "moinarz949@gmail.com"
current_directory = Path(__file__).resolve().parent
env_path = current_directory.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
email_password = os.getenv("EMAIL_PASSWORD")

subject = "Hello world"
body = """
    hello bro, how are you?
"""

em = EmailMessage()
em['From'] = email
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
    smtp.login(email,email_password)
    smtp.sendmail(email, email_receiver, em.as_string())