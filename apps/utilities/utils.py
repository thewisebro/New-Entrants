from django.core.mail import send_mail

def send_verification_mail(confirmation_key,email):
  print "mail_sending"
  email_subject = 'Account confirmation'
  email_body = " To verify your email address, click this link within 48hours http://channeli.in/#settings/email_auth/?confirm_key=%s" % (confirmation_key)
  send_mail(email_subject, email_body, 'channeli@iitr.ac.in',[email],fail_silently=False)

def mail_to_primary(email,primary_email):
  print "primary mail sending...."
  email1_subject = 'New Email address added for your channeli account.'
  email1_body = "A new Email address %s has been added to your channeli account." % (email)
  send_mail(email1_subject, email1_body, 'channeli@iitr.ac.in',[primary_email], fail_silently=False)

def send_passwordreset_mail(reset_key,email):
    print "mail_sending"
    email_subject = 'Password Reset'
    email_body = " To reset your password, click this link within 48hours http://channeli.in/#settings/password_reset/?reset_key=%s" % (reset_key)
    send_mail(email_subject, email_body, 'channeli@iitr.ac.in',[email],fail_silently=False)








