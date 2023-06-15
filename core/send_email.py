import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
def send_email(from_email,to_emails,subject,html_content):
	C=Mail(from_email=from_email,to_emails=to_emails,subject=subject,html_content=html_content)
	try:
		A=getattr(settings,'SENDGRID_API_KEY',None)
		if A:A=SendGridAPIClient(A);B=A.send(C);print(B.status_code);print(B.body);print(B.headers)
		else:print('SENDGRID_API_KEY not found in settings.py')
	except Exception as D:print(D.message)