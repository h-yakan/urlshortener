# Generated by Django 4.2.4 on 2023-08-31 14:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortenerapp', '0003_urls_expirationdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urls',
            name='expirationDate',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 8, 31, 14, 0, 3, 191319)),
        ),
    ]
