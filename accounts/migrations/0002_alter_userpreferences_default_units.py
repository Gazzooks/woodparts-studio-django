# Generated by Django 5.2.1 on 2025-06-04 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpreferences',
            name='default_units',
            field=models.CharField(choices=[('imperial', 'Imperial (inches)'), ('metric', 'Metric (mm)')], default='metric', max_length=10),
        ),
    ]
