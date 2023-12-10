# Generated by Django 5.0 on 2023-12-10 21:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Operations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sum_sent', models.IntegerField()),
                ('date', models.DateField()),
                ('reciever', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='reciever', to='accounts.account')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='sender', to='accounts.account')),
            ],
        ),
    ]
