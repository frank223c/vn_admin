# Generated by Django 2.0.3 on 2018-08-15 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cranedevices',
            options={'managed': False, 'verbose_name_plural': 'Crane Devices'},
        ),
        migrations.AlterModelOptions(
            name='cranetypes',
            options={'managed': False, 'verbose_name_plural': 'Crane Types'},
        ),
        migrations.AlterModelOptions(
            name='customers',
            options={'managed': False, 'verbose_name_plural': 'Customers'},
        ),
        migrations.AlterModelOptions(
            name='devices',
            options={'managed': False, 'verbose_name_plural': 'Devices'},
        ),
        migrations.AlterModelOptions(
            name='sitecranes',
            options={'managed': False, 'verbose_name_plural': 'Site Cranes'},
        ),
        migrations.AlterModelOptions(
            name='sites',
            options={'managed': False, 'verbose_name_plural': 'Sites'},
        ),
    ]
