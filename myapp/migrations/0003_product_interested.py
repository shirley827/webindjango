# Generated by Django 2.0.4 on 2018-06-04 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20180514_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='interested',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
