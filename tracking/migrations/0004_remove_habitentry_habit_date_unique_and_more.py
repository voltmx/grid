# Generated by Django 4.1.4 on 2023-09-04 04:06

from django.db import migrations, models
import django.db.models.functions.datetime


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0003_alter_habit_days_of_week'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='habitentry',
            name='habit_date_unique',
        ),
        migrations.AddConstraint(
            model_name='habitentry',
            constraint=models.UniqueConstraint(django.db.models.functions.datetime.TruncDate('date'), models.F('habit'), name='habit_date_unique'),
        ),
    ]
