from django.core.management.base import BaseCommand, CommandError
from buyandsell.cron_expire import move_to_expire

class Command(BaseCommand):
    args = ''
    help = 'Expire sell and request items after expiry date'

    def handle(self, *args, **options):
      move_to_expire()
