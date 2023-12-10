# Generated by Django 5.0 on 2023-12-08 11:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('users', '0003_user_saving_account_alter_user_bank_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='saving_account',
            field=models.OneToOneField(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='saving_account', to='accounts.account'),
        ),
    ]
