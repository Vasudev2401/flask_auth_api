import smtplib
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)


def send_email(recipient: str, subject: str, body: str) -> bool:
    sender = os.getenv("EMAIL_SENDER")
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if not all([sender, smtp_host, smtp_port, smtp_user, smtp_password]):
        raise ValueError("Missing required email configuration")

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)

            server.sendmail(
                sender,
                recipient,
                msg.as_string()
            )

        logging.info(f"Email sent successfully to {recipient}")
        return True

    except smtplib.SMTPAuthenticationError:
        logging.error("SMTP Authentication failed")

    except smtplib.SMTPConnectError:
        logging.error("SMTP connection failed")

    except smtplib.SMTPException as e:
        logging.error(f"SMTP error: {e}")

    except Exception as e:
        logging.error(f"Unexpected error: {e}")

    return False