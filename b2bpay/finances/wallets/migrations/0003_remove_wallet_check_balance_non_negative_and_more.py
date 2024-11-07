# Generated by Django 5.1.3 on 2024-11-07 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0002_wallet_check_balance_non_negative'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='wallet',
            name='check_balance_non_negative',
        ),
        migrations.AddConstraint(
            model_name='wallet',
            constraint=models.CheckConstraint(condition=models.Q(('balance__gte', 0)), name='wallet_balance_cant_be_negative'),
        ),
    ]
