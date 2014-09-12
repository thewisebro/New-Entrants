from django.core.management.base import BaseCommand, CommandError
from notices.cron_expire import move_to_expire

class Command(BaseCommand):
    args = ''
    help = 'Expire notices after expiry date'

    def handle(self, *args, **options):
      move_to_expire()
