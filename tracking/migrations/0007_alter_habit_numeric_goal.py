# Generated by Django 4.1.4 on 2023-09-13 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0006_alter_habitentry_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='numeric_goal',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
