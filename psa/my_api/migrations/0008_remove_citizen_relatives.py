# Generated by Django 2.2.3 on 2019-08-18 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_api', '0007_remove_citizen_import_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='citizen',
            name='relatives',
        ),
    ]
