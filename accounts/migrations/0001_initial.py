# Generated by Django 5.0 on 2023-12-07 17:07

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('account_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('is_activated', models.BooleanField(default=False)),
                ('saving_percent', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
            ],
        ),
    ]
