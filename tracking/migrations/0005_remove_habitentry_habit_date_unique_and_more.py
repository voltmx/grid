# Generated by Django 4.1.4 on 2023-09-09 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0004_remove_habitentry_habit_date_unique_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='habitentry',
            name='habit_date_unique',
        ),
        migrations.AlterField(
            model_name='habitentry',
            name='date',
            field=models.DateField(),
        ),
        migrations.AddConstraint(
            model_name='habitentry',
            constraint=models.UniqueConstraint(models.F('date'), models.F('habit'), name='habit_date_unique'),
        ),
    ]
