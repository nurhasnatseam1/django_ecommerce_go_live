# Generated by Django 3.0.5 on 2020-05-26 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0006_auto_20200501_2207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charge',
            name='refunded',
            field=models.BooleanField(default=False),
        ),
    ]