# Generated by Django 2.0.4 on 2018-06-20 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20180620_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='avatar',
            field=models.FileField(blank=True, default='image/default.PNG', max_length=300, null=True, upload_to='photo'),
        ),
    ]
