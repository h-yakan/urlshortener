# Generated by Django 4.2.3 on 2023-07-31 12:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortenerapp', '0007_alter_urls_datestarted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urls',
            name='dateStarted',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 31, 12, 8, 34, 873604, tzinfo=datetime.timezone.utc)),
        ),
    ]