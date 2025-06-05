# materials/management/commands/load_default_stock.py
from django.core.management.base import BaseCommand
from materials.models import StockMaterial
from materials.constants import IMPERIAL_LUMBER_SIZES, IMPERIAL_PLYWOOD_SIZES, METRIC_LUMBER_SIZES, METRIC_PLYWOOD_SIZES

class Command(BaseCommand):
    help = 'Loads default lumber and plywood stock into the database (both Imperial and Metric)'

    def handle(self, *args, **options):
        # Imperial materials
        for item in IMPERIAL_LUMBER_SIZES + IMPERIAL_PLYWOOD_SIZES:
            StockMaterial.objects.get_or_create(
                material=item['material'],
                thickness=item['thickness'],
                width=item['width'],
                length=item['length'],
                defaults={
                    'quantity': 10,
                    'price': 0,
                    'notes': item['notes'],
                    'unit_system': 'imperial',
                }
            )

        # Metric materials
        for item in METRIC_LUMBER_SIZES + METRIC_PLYWOOD_SIZES:
            StockMaterial.objects.get_or_create(
                material=item['material'],
                thickness=item['thickness'],
                width=item['width'],
                length=item['length'],
                defaults={
                    'quantity': 10,
                    'price': 0,
                    'notes': item['notes'],
                    'unit_system': 'metric',
                }
            )
