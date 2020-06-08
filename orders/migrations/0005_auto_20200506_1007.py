# Generated by Django 3.0.5 on 2020-05-06 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_productpurchase'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productpurchase',
            name='user',
        ),
        migrations.AddField(
            model_name='productpurchase',
            name='order',
            field=models.CharField(default='default order', max_length=120),
            preserve_default=False,
        ),
    ]