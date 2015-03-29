from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail

def send_verification_mail(request, confirmation_key, email):
  current_site = get_current_site(request)
  email_subject = 'Email verification'
  email_body = ("To verify your email address, click this link within 48hours"
                " %s/#settings/email_auth/?confirm_key=%s"
               ) % (current_site.domain, confirmation_key)
  send_mail(email_subject, email_body, 'channeli@iitr.ac.in',
            [email], fail_silently=False)

def mail_to_primary(request, email, primary_email):
  email1_subject = 'New Email address added for your Channel i account'
  email1_body = ("A new Email address %s has been added to your channeli"
                 " account.") % (email)
  send_mail(email1_subject, email1_body, 'channeli@iitr.ac.in',
            [primary_email], fail_silently=False)

def send_passwordreset_mail(request, reset_key, email):
  current_site = get_current_site(request)
  email_subject = 'Password Reset'
  email_body = ("To reset your password, click this link within 48hours "
                "%s/#settings/password_reset/?reset_key=%s"
               ) % (current_site.domain, reset_key)
  send_mail(email_subject, email_body, 'channeli@iitr.ac.in',
            [email], fail_silently=False)

