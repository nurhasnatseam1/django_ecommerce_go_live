# Generated by Django 3.0.5 on 2020-04-26 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='guestemail',
            old_name='timestam',
            new_name='timestamp',
        ),
    ]