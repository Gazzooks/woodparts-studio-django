# materials/models.py
from django.core.management.base import BaseCommand
from django.db import models

class StockMaterial(models.Model):
    material = models.CharField(max_length=100)
    length = models.FloatField()
    width = models.FloatField()
    thickness = models.FloatField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    unit_system = models.CharField(max_length=10, choices=[('imperial', 'Imperial'), ('metric', 'Metric')], default='metric')

    def __str__(self):
        return f"{self.material} ({self.length}x{self.width}x{self.thickness})"

class Command(BaseCommand):
    help = 'Loads default lumber and plywood stock into the database'

    def handle(self, *args, **options):
        # Common dimensional lumber (SPF, Pine, Cedar)
        lumber_sizes = [
            # (material, thickness, width, length, quantity, price, notes)
            ('SPF', 1.5, 3.5, 96, 20, 6.99, "2x4x8ft SPF Dimensional Lumber"),
            ('SPF', 1.5, 5.5, 96, 15, 8.99, "2x6x8ft SPF Dimensional Lumber"),
            ('SPF', 3.5, 3.5, 96, 10, 14.99, "4x4x8ft SPF Dimensional Lumber"),
            ('Pine', 0.75, 3.5, 96, 10, 5.99, "1x4x8ft Pine Board"),
            ('Cedar', 1.5, 5.5, 96, 8, 12.99, "2x6x8ft Cedar Dimensional Lumber"),
            # Add more as needed
        ]

        # Common plywood sheet sizes (thickness is actual)
        plywood_sizes = [
            # (material, thickness, width, length, quantity, price, notes)
            ('Plywood', 0.25, 48, 96, 10, 25.0, "1/4in x 4ft x 8ft Plywood Sheet"),
            ('Plywood', 0.5, 48, 96, 10, 35.0, "1/2in x 4ft x 8ft Plywood Sheet"),
            ('Plywood', 0.75, 48, 96, 10, 45.0, "3/4in x 4ft x 8ft Plywood Sheet"),
            # Add more as needed
        ]

        created = 0
        for item in lumber_sizes + plywood_sizes:
            material, thickness, width, length, quantity, price, notes = item
            obj, created_flag = StockMaterial.objects.get_or_create(
                material=material,
                thickness=thickness,
                width=width,
                length=length,
                defaults={
                    'quantity': quantity,
                    'price': price,
                    'notes': notes,
                }
            )
            if created_flag:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'Created: {obj}'))
            else:
                self.stdout.write(self.style.WARNING(f'Already exists: {obj}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {created} stock materials.'))