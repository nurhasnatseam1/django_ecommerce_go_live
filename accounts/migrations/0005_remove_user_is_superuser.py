# Generated by Django 3.0.5 on 2020-04-29 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200429_0851'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_superuser',
        ),
    ]
