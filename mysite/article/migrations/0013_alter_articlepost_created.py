# Generated by Django 4.2.9 on 2024-01-27 12:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0012_alter_articlepost_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 27, 12, 19, 28, 610702, tzinfo=datetime.timezone.utc)),
        ),
    ]
