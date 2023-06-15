import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
message=Mail(from_email='auto.email.activation@gmail.com',to_emails='suratiwan03@gmail.com',subject='Sending with Twilio SendGrid is Fun',html_content='<strong>Please verify your account...</strong>')
try:sg=SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'));response=sg.send(message);print(response.status_code);print(response.body);print(response.headers)
except Exception as e:print(e.message)