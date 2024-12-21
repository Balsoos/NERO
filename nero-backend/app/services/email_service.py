import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import Config

def send_email(to_email: str, subject: str, body: str):
    try:
        # Set up the email server
        server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
        server.starttls()  # Upgrade connection to secure

        # Log in to the email account
        server.login(Config.SMTP_USER, Config.SMTP_PASSWORD)

        # Create the email
        message = MIMEMultipart()
        message["From"] = Config.SMTP_USER
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Send the email
        server.sendmail(Config.SMTP_USER, to_email, message.as_string())
        server.quit()
        print(f"Email sent to {to_email} with subject '{subject}'")
    except Exception as e:
        print(f"Failed to send email: {e}")
