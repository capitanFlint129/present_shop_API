# Generated by Django 2.2.3 on 2019-08-18 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_api', '0003_auto_20190817_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citizen',
            name='gender',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=255),
        ),
    ]
