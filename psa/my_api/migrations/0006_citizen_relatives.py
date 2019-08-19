# Generated by Django 2.2.3 on 2019-08-18 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_api', '0005_remove_citizen_relatives'),
    ]

    operations = [
        migrations.AddField(
            model_name='citizen',
            name='relatives',
            field=models.ManyToManyField(related_name='_citizen_relatives_+', to='my_api.Citizen'),
        ),
    ]
