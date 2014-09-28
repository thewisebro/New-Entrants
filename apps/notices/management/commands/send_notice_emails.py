from django.core.management.base import BaseCommand, CommandError
from notices.cron_email import send_mails

class Command(BaseCommand):
  args = ''
  help = 'Sends notices emails'

  def handle(self, *args, **options):
    send_mails()
