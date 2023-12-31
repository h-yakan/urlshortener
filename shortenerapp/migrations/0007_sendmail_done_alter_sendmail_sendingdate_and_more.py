# Generated by Django 4.2.4 on 2023-08-31 14:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortenerapp', '0006_alter_sendmail_sendingdate_alter_urls_expirationdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='sendmail',
            name='done',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='sendmail',
            name='sendingDate',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 31, 14, 40, 12, 112999)),
        ),
        migrations.AlterField(
            model_name='urls',
            name='expirationDate',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 8, 31, 14, 40, 12, 111040)),
        ),
    ]
