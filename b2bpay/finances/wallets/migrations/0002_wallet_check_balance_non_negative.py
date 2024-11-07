# Generated by Django 5.1.3 on 2024-11-07 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='wallet',
            constraint=models.CheckConstraint(condition=models.Q(('balance__gte', 0)), name='check_balance_non_negative'),
        ),
    ]
