from django.core.mail import send_mail
from django.conf import settings

def get_link_domain():
  if not settings.PRODUCTION:
    sites = settings.DEVELOPMENT_SITES
  else:
    sites = settings.SITES
  if settings.SITE == 'INTERNET':
    return sites['INTERNET']['domain']
  else:
    return sites['INTRANET']['domain']

def send_verification_mail(confirmation_key, email):
  email_subject = 'Email verification'
  email_body = ("To verify your email address, click on the following link within 48 hours "
                " %s/#settings/email_auth/?confirm_key=%s"
               ) % (get_link_domain(), confirmation_key)
  send_mail(email_subject, email_body, 'channeli@iitr.ac.in',
            [email], fail_silently=False)

def mail_to_primary(email, primary_email):
  email1_subject = 'New Email address added for your Channel-i account'
  email1_body = ("A new Email address %s has been added to your channeli"
                 " account.") % (email)
  send_mail(email1_subject, email1_body, 'channeli@iitr.ac.in',
            [primary_email], fail_silently=False)

def send_passwordreset_mail(reset_key, email):
  email_subject = 'Password Reset'
  email_body = ("To reset your password, click on the following link within 48 hours "
                "%s/#settings/password_reset/?reset_key=%s"
               ) % (get_link_domain(), reset_key)
  send_mail(email_subject, email_body, 'channeli@iitr.ac.in',
            [email], fail_silently=False)
