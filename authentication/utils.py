
from django.core.mail import EmailMessage


def sendEmail(emailAddress, subject, body):
    email = EmailMessage(subject=subject, body=body, to=[emailAddress])
    email.send()

def sendRegistrationEmail(emailAddress,first_name, confirmationLink):
    subject = 'Welcome to Zbooni, confirm your email'
    body = "Hi"
    if first_name:
        body+=" "+first_name
    body += ",\nPlease click on this link to complete your regestration "+ confirmationLink +"\nBest"
    sendEmail(emailAddress, subject, body)