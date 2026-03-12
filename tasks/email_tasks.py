from extensions.celery_app import celery
from utils.email_sender import send_email
import os
from dotenv import load_dotenv
# from flask_jwt_extended import jwt_required

load_dotenv()

@celery.task(bind=True,autoretry_for=(Exception,),retry_backoff=60,retry_kwargs={"max_retries":3})
def send_verification_email(self,email,token):
    print("Sending verification email!!!")
    flask_port = os.getenv("FLASK_RUN_PORT")
    flask_host = os.getenv("FLASK_HOST")
    verification_link = f"http://{flask_host}:{flask_port}/auth/verify/{token}"
    subject = "Verify your Account"
    body = f"""
    Welcome!

    CLick the link below to verify your account:

    {verification_link}

    if you did not register , ignore this mail.
    """

    send_email(email,subject,body)


@celery.task(bind=True,autoretry_for=(Exception,),retry_backoff=60,retry_kwargs={"max_retries":3})
def send_role_change_email(self,email,new_role):
    print("Sending role change email!!!")
    subject = "Your role has been changed by admin!!"
    body = f"Your role has been changed to {new_role}"
    send_email(email,subject,body)


