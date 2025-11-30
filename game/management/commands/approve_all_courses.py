from django.core.management.base import BaseCommand
from game.models import Course

class Command(BaseCommand):
    help = 'Одобрить все существующие курсы'

    def handle(self, *args, **options):
        updated = Course.objects.filter(is_approved=False).update(is_approved=True)
        self.stdout.write(self.style.SUCCESS(f'Одобрено курсов: {updated}'))
